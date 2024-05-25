from rest_framework import serializers
from .models import Calender, CalenderComment
from user.serializers import UserSerializer
from project.serializers import ProjectSerializer

class CalenderSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    assign = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Calender
        fields = '__all__'

    def get_comments(self, instance):
        comments = CalenderComment.objects.filter(task=instance)
        serialized_comments = CalenderCommentSerializer(comments, many=True).data
        return serialized_comments

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = UserSerializer(instance.created_by).data
        representation['modified_by'] = UserSerializer(instance.modified_by).data
        representation['project'] = ProjectSerializer(instance.project).data
        return representation

class CalenderCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    end_date = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    assign = serializers.ListField(required=False)

    class Meta:
        model = Calender
        fields = '__all__'


class CalenderCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalenderComment
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_by'] = UserSerializer(instance.created_by).data
        return representation


class CalenderAddCommentSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)

