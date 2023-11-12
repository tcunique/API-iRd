from django.db import models

class Dag(models.Model):
    dag_id = models.CharField(max_length=255, primary_key=True)
    file_loc = models.CharField(max_length=255)
    has_import_errors = models.BooleanField()
    is_paused = models.BooleanField()
    is_active = models.BooleanField()
    is_subdag = models.BooleanField()
    next_dagrun = models.CharField(max_length=255)

    class Meta:
        managed = False