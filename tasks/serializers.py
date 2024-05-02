from rest_framework import serializers
from .models import Task, TaskURL
from user.serializers import UserSerializer
from project.serializers import ProjectSerializer

class TaskSerializer(serializers.ModelSerializer):
    urls = serializers.SerializerMethodField()
    assign = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def get_urls(self, instance):
        urls = TaskURL.objects.filter(task=instance)
        return [url.url for url in urls]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = UserSerializer(instance.created_by).data
        representation['modified_by'] = UserSerializer(instance.modified_by).data
        representation['project'] = ProjectSerializer(instance.project).data
        return representation
    

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'