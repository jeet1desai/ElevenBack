from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from .serializers import CalenderCreateSerializer, CalenderSerializer
from .models import Calender
from project.models import Project

class CalenderMethod(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        serializer = CalenderCreateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            startDate = datetime.strptime(start_date, '%Y-%m-%d %H:%M') if start_date else None
            endDate = datetime.strptime(end_date, '%Y-%m-%d %H:%M') if end_date else None

            calender = serializer.save(start_date=startDate, end_date=endDate, created_by=user, modified_by=user)
            serialized_calender = CalenderSerializer(calender).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_calender }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
        
class CalenderEvents(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            print(project)
            events = Calender.objects.filter(project=project, is_active=True)
            print(events)

            serialized_tasks = CalenderSerializer(events, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_tasks }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Project not found' }, status=status.HTTP_400_BAD_REQUEST)
        except Calender.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Calender not found' }, status=status.HTTP_400_BAD_REQUEST)