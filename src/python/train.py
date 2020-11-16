#!/usr/bin/env python
# coding: utf8
"""Example of training spaCy's named entity recognizer, starting off with an
existing model or a blank model.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
Last tested with: v2.2.4
"""
from __future__ import unicode_literals, print_function

import plac
import random
import warnings
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# training data
TRAIN_DATA = [
("Examples include: methanol; ethanol; n-propanol; isopropanol; n-butanol; isobutanol; sec-butanol; tertbutanol; 3-methyl-1-butanol; n-pentanol; isopentanol; amyl alcohol; iso-amyl alcohol; cyclopentanol; n-hexanol; cyclohexanol; 2-methyl-4-pentanol; heptanol; octanol; 2-ethyl hexanol; decanol; dodecanol; tetradecanol; hexdecanol; octandecanol; allyl alcohol; crotyl alcohol; methyl vinyl carbinol; or a mixture of two or more thereof.", {"entities": [(73, 83, "COMP")]}),
("Using the material from Example 6, a 30% by weight dispersion in isobutanol is prepared with stirring.", {"entities": [(65, 75, "COMP")]}),
("The carrier may be an organic solvent selected from (a) hydrocarbons, such as kerosene and fuel oils, n-pentane, cyclohexane, petroleum ether, petroleum benzine, benzene, xylene, toluene and mixtures thereof; (b) halogenated hydrocarbons, such as chlorobenzene, dichlorobenzene, bromobenzene and mixtures thereof; (c) alcohols, such as methanol, ethanol, n-propanol, n-butanol, isobutanol, benzylalcohol and mixtures thereof; (d) ethers such as diethyl ether, diisopropyl ether and mixtures thereof; (e) aldehydes, such as furfural and mixtures thereof; (f) ketones, such as acetone, ethyl methyl ketone and mixtures thereof; (g) fatty acids such as acetic acid, acetic anhydride and mixtures thereof and derivatives thereof; and (h) phenols, as well as mixtures of the various solvents.", {"entities": [(393, 403, "COMP")]}),
("A preferred use in accordance with this invention provides that the dihydroxylation is carried out in a solvent mixture containing one or more of the solvents of the group: water, alcohols such as methanol, ethanol, isopropanol, N-propanol, N-butanol, secondary butanol, tert.-butanol, isobutanol, N-pentanol; ethers such as diethylether, tetrahydrofuran, dimethoxy ethane, dioxane; ketones such as acetone, methyl isobutyl ketone, ethyl ketone (sic), diisopropyl ketone; or esters such as acetyl acetic esters or acetic esters, as well as halogenated alkanes such as methylene chloride, chloroform, and trichlorethylene.", {"entities": [(287, 297, "COMP")]}),
("Compound (162) was prepared in the manner of example 87 with the following substitutions: 6-(2'S-t-butoxycarbonyl amino-1'-oxo-propylamino)-3-(4-pyridyl)-2-(4-fluoro phenyl)-7-aza-indole was used in place of 6-(2'-t-butoxycarbonylamino-1'-oxo-ethylamino)-3-(4-pyridyl)-2-(4-fluorophenyl)-7-aza-indole and isobutanol was used in place of methanol which afforded 6-(2'S-amino-1'-oxo-propylamino)-3-(4-pyridyl)-2-(4-fluorophenyl)-1-isobutyl-7-aza-indole (162) after preparative plate chromatography: Mass Spectrum (CI) 432 (MH+).", {"entities": [(306, 316, "COMP")]}),
("Especially preferred solvents are selected from: methanol, ethanol, isopropanol, n-butanol, isobutanol and acetonitrile.", {"entities": [(92, 102, "COMP")]}),
("-- DIPEDA    isobutanol  73      94            61.0        83.2", {"entities": [(13, 23, "COMP")]}),
("Such solvents include isopropanol, isobutanol, isopropyl acetate, butyl acetate, acetone and acetonitrile.", {"entities": [(35, 45, "COMP")]}),
("1 g of racemic 6-(4-aminophenyl)-4,5-dihydro-5-methyl-3(2H)-pyridazinone was added to 20 ml of isobutanol and 0.75 g of L-tartaric acid.", {"entities": [(95, 105, "PERSON")]}),
("isobutanol 5-1", {"entities": [(0, 10, "COMP")]}),
("-- 3) Melamine resin from Hoechst AG; 55% solution in isobutanol", {"entities": [(54, 64, "COMP")]}),
]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir=None, n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    # only train NER
    with nlp.disable_pipes(*other_pipes), warnings.catch_warnings():
        # show warnings for misaligned entity spans once
        warnings.filterwarnings("once", category=UserWarning, module='spacy')

        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == "__main__":
    plac.call(main)

    # Expected output:
    # Entities [('Shaka Khan', 'PERSON')]
    # Tokens [('Who', '', 2), ('is', '', 2), ('Shaka', 'PERSON', 3),
    # ('Khan', 'PERSON', 1), ('?', '', 2)]
    # Entities [('London', 'LOC'), ('Berlin', 'LOC')]
    # Tokens [('I', '', 2), ('like', '', 2), ('London', 'LOC', 3),
    # ('and', '', 2), ('Berlin', 'LOC', 3), ('.', '', 2)]
