import subprocess
import time
import sys
from random import random
from operator import add
from pyspark.sql import SparkSession
from namedEntityRecognition.namedEntityRecognition import hash_model, get_ner
from database.database import persist_data, get_patent, save_ner

from config.config import sparkToken, sparkSubmit, k8sendpoint

sparkToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IlVJdFRxTHNHb294NXB2OVRyZzgzZVZzRm5QMHVWbGxRYVlYZmdlUlZUNzQifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6InNwYXJrLXRva2VuLXN6MmQ3Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6InNwYXJrIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZjg2MThmZGUtN2ZmZi00NjkwLTk0M2YtMWM2M2ZkYzY1OGVmIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50OmRlZmF1bHQ6c3BhcmsifQ.MNc2WOmUTE7qZocIBM9U61wnDD31aKCKSqHSQsGEmIQFMymOqO5VBkJuHidnHqR-lvWBeEupz1td6JTUbU6nDiFIUwGTO3c4Jy4iByeW4jKeA4zP60Mx6MwWcwjgTCMFtKLCiC86vQlNSLq4v2aD0KLiIozcqHpU9tz2G81MHoP5l-OuKhSrhQcxE3uZEdg2gRUUAP5_k33rAhQZbdNSGj_jl_GJDLLZmnZwlhuBX1ARiinyE7Raiq8n01eAJ8grLz0NEjR4qpSZoqiI-ZSV3uTxvTuJt_BC5aWuGY2f7h93Ba2XwPed4nSa0ndWP7ra0p2L4CcoAu5h0rCxU2eWqQ'
sparkSubmit= '/tmp/spark-3.0.1-bin-hadoop2.7/bin/spark-submit'
k8sendpoint='localhost'
listPatents=["patent1", "patent2"]

def launch_spark(listPatents):
    subprocess.call( [
        sparkSubmit,
        '--deploy-mode', 'cluster',
        '--master', 'k8s://https://' + k8sendpoint + ':8443',
        '--name', 'nerkernel',
        '--conf', 'spark.kubernetes.authenticate.driver.serviceAccountName=spark',
        '--conf', 'spark.kubernetes.authenticate.submission.oauthToken=' + sparkToken,
        '--conf', 'spark.executor.instances=5',
        '--conf', 'spark.kubernetes.driver.container.image=spark-py:latest',
        '--conf', 'spark.kubernetes.executor.container.image=spark-py:latest',
        '--conf', 'spark.kubernetes.container.image=spark-py:latest',
        '--conf', 'spark.kubernetes.container.imagePullPolicy=IfNotPresent',
        '--conf', 'spark.kubernetes.driver.volumes.persistentVolumeClaim.volume.mount.path=/opt/spark/shared-pvc',
        '--conf', 'spark.kubernetes.driver.volumes.persistentVolumeClaim.volume.mount.readOnly=false',
        '--conf', 'spark.kubernetes.driver.volumes.persistentVolumeClaim.volume.mount.claimName=shared-pvc',
        '--conf', 'spark.kubernetes.executor.volumes.persistentVolumeClaim.volume.mount.path=/opt/spark/shared-pvc',
        '--conf', 'spark.kubernetes.executor.volumes.persistentVolumeClaim.volume.mount.readOnly=false',
        '--conf', 'spark.kubernetes.executor.volumes.persistentVolumeClaim.volume.mount.claimName=shared-pvc',
        'local:///opt/app/nerproject/src/python/sparkLauncher/sparkLauncher.py',
        "[" + ( ','.join( map( lambda x: '"' + x + '"', listPatents ) ) ) + "]"
    ] )

   /tmp/spark-3.0.1-bin-hadoop2.7/bin/spark-submit \
   --deploy-mode cluster \
   --master k8s://https://localhost:8443 \
   --name nerkernel \
   --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
   --conf spark.executor.instances=5 \
   --conf spark.kubernetes.driver.container.image=nerproject:latest \
   --conf spark.kubernetes.executor.container.image=nerproject:latest \
   --conf spark.kubernetes.container.image=nerproject:latest \
   --conf spark.kubernetes.container.imagePullPolicy=IfNotPresent \
   --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.volume.mount.path=/opt/spark/shared-pvc \
   --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.volume.mount.readOnly=false \
   --conf spark.kubernetes.driver.volumes.persistentVolumeClaim.volume.options.claimName=shared-pvc \
   --conf spark.kubernetes.executor.volumes.persistentVolumeClaim.volume.mount.path=/opt/spark/shared-pvc \
   --conf spark.kubernetes.executor.volumes.persistentVolumeClaim.volume.mount.readOnly=false \
   --conf spark.kubernetes.executor.volumes.persistentVolumeClaim.volume.options.claimName=shared-pvc \
   --conf spark.executorEnv.PYTHONPATH=/opt/app/nerproject/src/python \
   --conf spark.driverEnv.PYTHONPATH=/opt/app/nerproject/src/python \
   local:///opt/app/nerproject/src/python/sparkLauncher/sparkLauncher.py \
   '["patent1","patent2"]'

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("nerkernel")\
        .getOrCreate()

    partitions = eval(sys.argv[1])

    def kernel(patentId):
        print("Processing patent " + patentId)
        # document = get_patent(patentId)
        # ner = get_ner( document )
        # save_ner( ner, hash_model() )

        time.sleep(10)

        return 1

    count = spark.sparkContext.parallelize(partitions, len(partitions)).map(kernel).reduce(add)

    spark.stop()

