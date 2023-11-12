from django.shortcuts import render


import requests
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django_api import settings
from django_.models import Dag
from django_.serializers import DagSerializer

@csrf_exempt
def airflow_dags(request):
    if request.method == 'GET':
            
        # On donne les identifiants de connexion à l'API d'Apache Airflow
        username = 'airflow'
        password = 'airflow'

        # On créee l'URL de l'API d'Apache Airflow
        url = f'{settings.AIRFLOW_BASE_URL}/dags'

        # On fait la requête à l'API d'Apache Airflow
        response = requests.get(url, auth=(username, password))

        # On vérifie que la requête a bien fonctionné
        if response.status_code == 200:
            # On récupère les données de la réponse
            # Utilise protocole http, une requête, une destination, je crée une requête dans le get, avec l'url, le corp, le chemin où je veux aller.
            # M7 vont nous envoyer uenr euqête, et va mettre en contenu, dans le body, du json, du text json. HTTP arrive au nvx de l'api, et api
            # à un point qui puisse recevoir cette information là. 
            # J'ai crée des points d'entrée, et eux vont pouvoir communiquer avec. 
            dags_data = response.json().get('dags', [])

            # On crée une liste de modèle Dag à partir des données
            dags = [Dag(dag_id=dag['dag_id'], file_loc=dag['fileloc'], has_import_errors=dag['has_import_errors'], is_paused=dag['is_paused'], is_active=dag['is_active'], is_subdag=dag['is_subdag'], next_dagrun=dag['next_dagrun']) for dag in dags_data]

            # Trier les DAGs par ordre alphabétique
            dags_sorted = sorted(dags, key=lambda dag: dag.dag_id)

            # Utiliser le serializer pour convertir les objets Dag en JSON
            serializer = DagSerializer(dags_sorted, many=True)

            # Créer le résultat sous forme de dict
            result = {
                'message': 'Liste des DAGs Apache Airflow',
                'dags': serializer.data
            }

            # Retourner la réponse JSON
            return JsonResponse(result)
        else:
            error_message = f'Failed to fetch DAGs from Apache Airflow API: {response.status_code}'
            return JsonResponse({'error': error_message})
    
@csrf_exempt
def delete_dags(request, dag_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Only DELETE method is allowed'})
    username = 'airflow'
    password = 'airflow'
    url = f'{settings.AIRFLOW_BASE_URL}/dags/' + dag_id
    response = requests.delete(url, auth=(username, password))

    if response.status_code == 204:
        return JsonResponse({'success': 'DAG deleted successfully'})
    else:
        return JsonResponse({'error': 'Failed to delete DAG from Apache Airflow API'})


@csrf_exempt
def launch(request, dag_id):
    if request.method != 'PATCH':
        return JsonResponse({'error': 'Only PATCH method is allowed'})
    # On donne les identifiants de connexion à l'API d'Apache Airflow
    username = 'airflow'
    password = 'airflow'

    # On créee l'URL de l'API d'Apache Airflow
    url = f'{settings.AIRFLOW_BASE_URL}/dags/' + dag_id

    # Préparer les données à envoyer
    data = {
        "is_paused": True,
    }

    # On fait la requête à l'API d'Apache Airflow
    response = requests.patch(url, auth=(username, password), json=data)

    # On vérifie que la requête a bien fonctionné
    if response.status_code == 200:
        return JsonResponse({'success': 'DAG triggered successfully'})
    else:
        error_message = f'Failed to trigger DAG from Apache Airflow API: {response.status_code}'
        return JsonResponse({'error': error_message})
    
@csrf_exempt
def pause(request, dag_id):
    if request.method != 'PATCH':
        return JsonResponse({'error': 'Only PATCH method is allowed'})
    # On donne les identifiants de connexion à l'API d'Apache Airflow
    username = 'airflow'
    password = 'airflow'

    # On créee l'URL de l'API d'Apache Airflow
    url = f'{settings.AIRFLOW_BASE_URL}/dags/' + dag_id

    # Préparer les données à envoyer
    data = {
        "is_paused": False,
    }

    # On fait la requête à l'API d'Apache Airflow
    response = requests.patch(url, auth=(username, password), json=data)    

    # On vérifie que la requête a bien fonctionné
    if response.status_code == 200:
        return JsonResponse({'success': 'DAG paused successfully'})
    else:
        error_message = f'Failed to pause DAG from Apache Airflow API: {response.status_code}'
        return JsonResponse({'error': error_message})


@csrf_exempt
def create_dag(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            url = f'{settings.AIRFLOW_BASE_URL}/dags/{settings.DAG_TEMPLATE}/dagRuns'
            username = 'airflow'
            password = 'airflow'

            # preparing data to send
            data = {
                "conf": json_data
            }

            # send JSON to Apache Airflow
            response = requests.post(url, auth=(username, password), json=data)

            # test pour voir si le json est bien envoyé
            if response.status_code == 200 or response.status_code == 201:
                return JsonResponse({'success': 'JSON sent successfully'})
            else:
                error_message = f'Failed to send JSON from Apache Airflow API: {response.status_code}'
                return JsonResponse({'error': error_message})
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Méthode de requête invalide'}, status=405)


from django.http import JsonResponse
from .task import check_dag_status_task

@csrf_exempt
def check_dag_status(request):
    # Appeler la tâche Celery pour récupérer les données du DAG
    dags_data = check_dag_status_task.delay().get()

    # On crée une liste de modèle Dag à partir des données
    dags = [Dag(dag_id=dags_data['dag_id'], file_loc=dags_data['fileloc'], has_import_errors=dags_data['has_import_errors'], is_paused=dags_data['is_paused'], is_active=dags_data['is_active'], is_subdag=dags_data['is_subdag'], next_dagrun=dags_data['next_dagrun'])]

    # Utiliser le serializer pour convertir les objets Dag en JSON
    serializer = DagSerializer(dags, many=True)

    # Retourner l'état de la dernière exécution du DAG dans la réponse JSON
    return JsonResponse(serializer.data, safe=False)