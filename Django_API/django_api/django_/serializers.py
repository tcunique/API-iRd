from rest_framework import serializers
from django_.models import Dag

class DagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dag
        fields = ['dag_id', 'file_loc', 'has_import_errors', 'is_paused', 'is_active', 'is_subdag', 'next_dagrun']

