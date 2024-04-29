from rest_framework import serializers
from .models import Project, Membership
from user.serializers import UserSerializer, CompSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = UserSerializer(instance.created_by).data
        representation['modified_by'] = UserSerializer(instance.modified_by).data
        return representation
    

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['project'] = ProjectSerializer(instance.project).data
        representation['company'] = CompSerializer(instance.company).data
        representation['modified_by'] = UserSerializer(instance.modified_by).data
        return representation


class CreateProjectSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    status = serializers.IntegerField(required=True)
    code = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    start_date = serializers.CharField(required=False, allow_blank=True)
    end_date = serializers.CharField(required=False, allow_blank=True)