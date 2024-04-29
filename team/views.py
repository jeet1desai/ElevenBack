from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from project.models import Project, Membership
from project.serializers import MembershipSerializer

class Teams(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            memberships = Membership.objects.filter(project__id=project_id)
            serialized_membership = MembershipSerializer(memberships, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_membership }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found" }, status=status.HTTP_404_NOT_FOUND)
        
    permission_classes = [IsAuthenticated]
    def delete(self, request, project_id, user_id, format=None):
        user = request.user
        try:
            membership = Membership.objects.filter(project__id=project_id, user__id=user_id)
            membership.delete()
            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success" }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found" }, status=status.HTTP_404_NOT_FOUND)
