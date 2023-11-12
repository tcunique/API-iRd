from __future__ import absolute_import
import os
from celery import Celery
from django_api import settings
from datetime import timedelta
from datetime import datetime
from celery.signals import worker_ready

# permet à Celery de charger les paramètres de configuration de l'application Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_api.settings')

# crée une instance de la classe Celery avec le nom de l'application 'django_api'.
app = Celery('django_api')

app.config_from_object('django.conf:settings', namespace='CELERY')

# donner toutes les tâches disponibles dans ontre api django
app.autodiscover_tasks()

now = datetime.utcnow()  # Obtenez l'heure actuelle en UTC

app.conf.beat_schedule = {
    'check_dag_status_every_hours': {
        'task': 'django_.task.check_dag_status_task',
        'schedule': timedelta(hours = 1),
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

#Pour exécuter au moins une fois la tâche check_dag_status_task
@worker_ready.connect
def execute_task_immediately(sender, **kwargs):
    sender.app.send_task('django_.task.check_dag_status_task')