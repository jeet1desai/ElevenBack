from rest_framework import serializers
from user.models import User
from project.models import Project
from .models import Document
from user.serializers import UserSerializer

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['modified_by'] = UserSerializer(instance.modified_by).data
        return representation

class CreateDocumentSerializer(serializers.Serializer):
    userId = serializers.IntegerField(required=True)
    projectId = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    type = serializers.CharField(required=True)
    url = serializers.CharField(required=True)
    is_published = serializers.BooleanField(required=True)

    def validate(self, attrs):
        user_id = attrs.get("userId")
        project_id = attrs.get('projectId')

        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found.')
        try:
            project = Project.objects.get(id=project_id, is_active=True)
        except Project.DoesNotExist:
            raise serializers.ValidationError('Project not found.')

        return attrs


class DeleteDocumentSerializer(serializers.Serializer):
    docId = serializers.IntegerField(required=True)
    role = serializers.IntegerField(required=True)
    projectId = serializers.IntegerField(required=True)

    def validate(self, attrs):
        doc_id = attrs.get("docId")
        try:
            document = Document.objects.get(id=doc_id, is_active=True)
        except Document.DoesNotExist:
            raise serializers.ValidationError('Document not found.')
        return attrs
    

class PublishDocumentSerializer(serializers.Serializer):
    docId = serializers.IntegerField(required=True)
    role = serializers.IntegerField(required=True)
    projectId = serializers.IntegerField(required=True)
    isPublish = serializers.BooleanField(required=True)

    def validate(self, attrs):
        doc_id = attrs.get("docId")
        try:
            document = Document.objects.get(id=doc_id, is_active=True)
        except Document.DoesNotExist:
            raise serializers.ValidationError('Document not found.')
        return attrs