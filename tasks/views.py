from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import TaskCreateSerializer, TaskSerializer
from .models import TaskURL, Task
from django.utils import timezone

class Tasks(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(created_by=user, modified_by=user)
            
            urls = request.data.get('url', [])
            if urls:
                for url in urls:
                    task_url = TaskURL.objects.create(task=task, url=url)

            serialized_task = TaskSerializer(task).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_task }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': "Something went wrong" }, status=status.HTTP_400_BAD_REQUEST)
        

    permission_classes = [IsAuthenticated]
    def put(self, request, task_id, format=None):
        user = request.user
        try:
            task = Task.objects.get(id=task_id, is_active=True)
            serializer = TaskCreateSerializer(task, data=request.data)
            if serializer.is_valid():
                serializer.save(modified_by=request.user, modified_date=timezone.now())

                urls = request.data.get('url', [])
                if urls:
                    task.urls.all().delete()
                    for url in urls:
                        TaskURL.objects.create(task=task, url=url)

                serialized_task = TaskSerializer(task).data
                return Response({'status': status.HTTP_200_OK, 'msg': 'Task updated successfully', 'data': serialized_task }, status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
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
            return Response({'status': status.HTTP_200_OK, 'msg': 'Task deleted successfully', 'data': serialized_task }, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Task not found'}, status=status.HTTP_400_BAD_REQUEST)

