from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from .serializers import CalenderCreateSerializer, CalenderSerializer, CalenderAddCommentSerializer, CalenderCommentSerializer
from .models import Calender, CalenderComment
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


    permission_classes = [IsAuthenticated]
    def put(self, request, calender_id, format=None):
        user = request.user
        try:
            calendar = Calender.objects.get(id=calender_id, is_active=True)
            serializer = CalenderCreateSerializer(calendar, data=request.data)
            if serializer.is_valid():
                start_date = request.data.get('start_date')
                end_date = request.data.get('end_date')

                startDate = datetime.strptime(start_date, '%Y-%m-%d %H:%M') if start_date else None
                endDate = datetime.strptime(end_date, '%Y-%m-%d %H:%M') if end_date else None

                serializer.save(start_date=startDate, end_date=endDate, modified_by=user, modified_date=timezone.now())

                serialized_calendar = CalenderSerializer(calendar).data
                return Response({'status': status.HTTP_200_OK, 'msg': 'Calender updated successfully', 'data': serialized_calendar }, status=status.HTTP_200_OK)
            else:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)
        except Calender.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': "Calender not found"}, status=status.HTTP_400_BAD_REQUEST)


    permission_classes = [IsAuthenticated]
    def delete(self, request, calender_id, format=None):
        user = request.user
        try:
            calendar = Calender.objects.get(id=calender_id, is_active=True)
            calendar.is_active = False
            calendar.modified_by = user
            calendar.modified_date = timezone.now()
            calendar.save()

            serialized_calendar = CalenderSerializer(calendar).data
            return Response({'status': status.HTTP_200_OK, 'msg': 'Calender deleted successfully', 'data': serialized_calendar }, status=status.HTTP_200_OK)
        except Calender.DoesNotExist:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Calender not found'}, status=status.HTTP_400_BAD_REQUEST)


class CalenderEvents(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            events = Calender.objects.filter(project=project, is_active=True).filter(
                Q(created_by=user) | Q(assign=user) | Q(assign__isnull=True)
            ).distinct()
            serialized_calendars = CalenderSerializer(events, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_calendars }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Project not found' }, status=status.HTTP_400_BAD_REQUEST)
        except Calender.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Calender not found' }, status=status.HTTP_400_BAD_REQUEST)


class CalenderComments(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, calender_id, format=None):
        user = request.user
        try:
            calendar = Calender.objects.get(id=calender_id, is_active=True)
            serializer = CalenderAddCommentSerializer(data=request.data)
            if serializer.is_valid():
                comment = request.data.get('comment')
                comment_instance = CalenderComment.objects.create(comment=comment, calender=calendar, created_by=user)
                serialized_comment = CalenderCommentSerializer(comment_instance).data
                return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_comment }, status=status.HTTP_200_OK)
            else:
                return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)
        except Calender.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Calender not found' }, status=status.HTTP_400_BAD_REQUEST)
