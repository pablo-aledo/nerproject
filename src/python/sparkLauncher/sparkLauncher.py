import subprocess

from config.config import sparkToken, sparkSubmit

def launch_spark():
    subprocess.call( [
        sparkSubmit,
        '--deploy-mode', 'cluster',
        '--master', 'k8s://https://localhost:8443',
        '--name', 'sparkpi',
        '--conf', 'spark.kubernetes.authenticate.driver.serviceAccountName=spark',
        '--conf', 'spark.kubernetes.authenticate.submission.oauthToken=' + sparkToken,
        '--conf', 'spark.executor.instances=5',
        '--conf', 'spark.kubernetes.driver.container.image=spark-py:latest',
        '--conf', 'spark.kubernetes.executor.container.image=spark-py:latest',
        '--conf', 'spark.kubernetes.container.image=spark-py:latest',
        '--conf', 'spark.kubernetes.container.imagePullPolicy=IfNotPresent',
        'local:///opt/spark/examples/src/main/python/pi.py',
        '100'
    ] )
