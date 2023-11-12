from airflow import DAG
import json
from django.http import HttpResponse
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 22),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

#Je veux une fonction qui renvoie un dictionnaire de taches et de leurs parametres
# de la forme suivante : 
# [{name : "tache1", program : "nom_fichier1.py", args : {arg1: val1,  arg2 : val2 , arg3 : val3 }},
#  {name : "tache2", program : "nom_fichier2.py", args : {arg1: val1,  arg2 : val2 , arg3 : val3 }}
# ...]
#Elle doit lire ces informations dans un fichier json reçu en parametre

def lire_fichier_json(fichier): #request est le nom d'un fichier json reçu que je vais lire
    with open(fichier) as f:
        data = json.load(f)
    return HttpResponse(json.dumps(data), content_type='application/json') 

args = lire_fichier_json(request) #request est le nom d'un fichier json reçu que je vais lire
op_kwargs = args #args est le dictionnaire de taches et de leurs parametres


dag = DAG_template(
    'example_dag',
    default_args=default_args,
    description='An example DAG',
    schedule_interval=timedelta(days=1),
)

t1 = PythonOperator(
    task_id='run_task',
    bash_command='date',
    dag=dag,
)

t2 = BashOperator(
    task_id='sleep',
    depends_on_past=False,
    bash_command='sleep 5',
    retries=3,
    dag=dag,
)

t1 >> t2