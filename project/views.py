from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Membership
from .serializers import ProjectSerializer
from rest_framework import status
from rest_framework.response import Response

class Projects(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        try:
            memberships = Membership.objects.filter(user=user)
            if memberships.exists():
                projects = [membership.project for membership in memberships]
                serialized_projects = ProjectSerializer(projects, many=True).data
                return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_projects }, status=status.HTTP_200_OK)
        except Membership.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found" }, status=status.HTTP_404_NOT_FOUND)
