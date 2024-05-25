from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from .serializers import CalenderCreateSerializer, CalenderSerializer

class Calender(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        serializer = CalenderCreateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            startDate = datetime.strptime(start_date, '%Y-%m-%d') if start_date else None
            endDate = datetime.strptime(end_date, '%Y-%m-%d') if end_date else None
            calender = serializer.save(start_date=startDate, end_date=endDate, created_by=user, modified_by=user)
              
            serialized_calender = CalenderSerializer(calender).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_calender }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)