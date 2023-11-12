import json
from datetime import datetime 

from airflow import DAG 
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator


with DAG(
    dag_id='example',
    schedule_interval='@daily',
    start_date=datetime(2021, 1, 1),
    catchup=False
) as dag:
    
    task_api_is_active = HttpSensor(
        task_id='api_is_active',
        http_conn_id='api_posts',
        # Rajoute /posts après le lien host que nous avons rentré dans le dossier connexion sur apache airflow
        endpoint='posts'
    )

    task_get_posts = SimpleHttpOperator(
        task_id='get_posts',
        # Extrêmemnt important da'voir la bonne orthographe sinon ça provoque des erreurs
        http_conn_id='api_posts',
        endpoint='posts',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    task_print_posts = PythonOperator(
        task_id='print_posts',
        python_callable=lambda x: print(x),
        op_kwargs={'x': '{{ task_instance.xcom_pull(task_ids="get_posts") }}'}
    )

    task_api_is_active >> task_get_posts >> task_print_posts