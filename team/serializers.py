from rest_framework import serializers
from user.models import User
from project.models import Project

class UpdateRoleSerializer(serializers.Serializer):
    userId = serializers.IntegerField(required=True)
    projectId = serializers.IntegerField(required=True)
    role = serializers.IntegerField(required=True)

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
