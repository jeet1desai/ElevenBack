from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import TaskCreateSerializer, TaskSerializer, TaskAddCommentSerializer, TaskCommentSerializer
from .models import TaskURL, Task, TaskComment
from project.models import Project
from django.utils import timezone
from datetime import datetime


class Tasks(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            startDate = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
            endDate = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
            task = serializer.save(start_date=startDate, end_date=endDate, created_by=user, modified_by=user)
            
            urls = request.data.get('url', [])
            if urls:
                for url in urls:
                    task_url = TaskURL.objects.create(task=task, url=url)

            serialized_task = TaskSerializer(task).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_task }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = [IsAuthenticated]
    def put(self, request, task_id, format=None):
        user = request.user
        try:
            task = Task.objects.get(id=task_id, is_active=True)
            serializer = TaskCreateSerializer(task, data=request.data)
            if serializer.is_valid():
                start_date = request.data.get('start_date')
                end_date = request.data.get('end_date')
                startDate = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
                endDate = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
                serializer.save(start_date=startDate, end_date=endDate, modified_by=request.user, modified_date=timezone.now())

                urls = request.data.get('url', [])
                if urls:
                    task.urls.all().delete()
                    for url in urls:
                        TaskURL.objects.create(task=task, url=url)

                serialized_task = TaskSerializer(task).data
                return Response({'status': status.HTTP_200_OK, 'msg': 'Task updated successfully', 'data': serialized_task }, status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': "Task not found"}, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = [IsAuthenticated]
    def delete(self, request, task_id, format=None):
        user = request.user
        try:
            task = Task.objects.get(id=task_id, is_active=True)
            task.is_active = False
            task.modified_by = user
            task.modified_date = timezone.now()
            task.save()

            serialized_task = TaskSerializer(task).data
            return Response({'status': status.HTTP_200_OK, 'msg': 'Task deleted successfully', 'data': serialized_task }, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Task not found'}, status=status.HTTP_400_BAD_REQUEST)


    permission_classes = [IsAuthenticated]
    def get(self, request, task_id, format=None):
        user = request.user
        try:
            task = Task.objects.get(id=task_id, is_active=True)
            serialized_task = TaskSerializer(task).data
            return Response({'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_task }, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Task not found'}, status=status.HTTP_400_BAD_REQUEST)


class GetTeamTasks(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            tasks = Task.objects.filter(project=project, is_active=True)
            serialized_tasks = TaskSerializer(tasks, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_tasks }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Project not found' }, status=status.HTTP_400_BAD_REQUEST)


class GetMyTasks(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            tasks = Task.objects.filter(project=project, assign=user, is_active=True)
            serialized_tasks = TaskSerializer(tasks, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_tasks }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Project not found' }, status=status.HTTP_400_BAD_REQUEST)


class TaskComments(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, task_id, format=None):
        user = request.user
        try:
            task = Task.objects.get(id=task_id, is_active=True)
            serializer = TaskAddCommentSerializer(data=request.data)
            if serializer.is_valid():
                comment = request.data.get('comment')
                comment_instance = TaskComment.objects.create(comment=comment, task=task, created_by=user)
                serialized_comment = TaskCommentSerializer(comment_instance).data
                return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_comment }, status=status.HTTP_200_OK)
            else:
                return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Task not found' }, status=status.HTTP_400_BAD_REQUEST)
