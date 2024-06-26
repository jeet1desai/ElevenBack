from rest_framework import serializers
from .models import Task, TaskComment
from user.serializers import UserSerializer
from project.serializers import ProjectSerializer

class TaskSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    assign = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def get_comments(self, instance):
        comments = TaskComment.objects.filter(task=instance)
        serialized_comments = TaskCommentSerializer(comments, many=True).data
        return serialized_comments

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = UserSerializer(instance.created_by).data
        representation['modified_by'] = UserSerializer(instance.modified_by).data
        representation['project'] = ProjectSerializer(instance.project).data
        return representation


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = UserSerializer(instance.created_by).data
        return representation


class TaskCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    end_date = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    assign = serializers.ListField(required=False)

    class Meta:
        model = Task
        fields = '__all__'


class TaskAddCommentSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)

