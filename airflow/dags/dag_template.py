from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator


def recupere_dico(**kwargs):
    json_data = kwargs['dag_run'].conf
    tasks = json_data.get('taches', {})
    if tasks:
        t1 = BashOperator(
            task_id=tasks['nom_tache'],
            bash_command=f"python3 {tasks['chemin_fichier']} {tasks['args']}",
            dag=kwargs['dag']
    ).execute(context=kwargs)


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id='dag_template',
    schedule_interval='@daily',
    default_args=default_args,
    start_date=datetime(2021, 1, 1),
    catchup=False
) as dag:
    
    tache1 = PythonOperator(
        task_id='tache1',
        python_callable=recupere_dico,
        dag=dag
    )

    tache1