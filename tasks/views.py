from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from .serializers import TaskCreateSerializer, TaskSerializer
from .models import TaskURL

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
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
