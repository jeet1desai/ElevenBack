from rest_framework import serializers
from .models import Project
from user.serializers import UserSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = UserSerializer(instance.created_by).data
        representation['modified_by'] = UserSerializer(instance.modified_by).data
        return representation
