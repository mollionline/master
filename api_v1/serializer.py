from issue_tracker.models import Project, Task
from rest_framework import serializers


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project', 'description', 'created_at', 'updated_at', 'is_deleted', 'user']
        read_only_fields = ['id']


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'summary', 'description', 'status',
            'created_at', 'updated_at', 'is_deleted',
            'type', 'project'
        ]
        read_only_fields = ['id']
