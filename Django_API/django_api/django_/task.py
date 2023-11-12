from celery import shared_task
from django_api import settings
import requests
# Importez ici les autres dépendances nécessaires

@shared_task
def check_dag_status_task():
    # Copiez ici la logique principale de la fonction de vue check_dag_status
    dag_runs_url = f"{settings.AIRFLOW_BASE_URL}/dags/{settings.DAG_TEMPLATE}"
    username = 'airflow'
    password = 'airflow'
    response = requests.get(dag_runs_url, auth=(username, password))
    dags_data = response.json()
    
    return dags_data

