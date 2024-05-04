from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from project.models import Project, Membership
from project.serializers import MembershipSerializer
from .serializers import UpdateRoleSerializer, TeamMemberSerializer

class Teams(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            memberships = Membership.objects.filter(project=project)
            serialized_membership = MembershipSerializer(memberships, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_membership }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found" }, status=status.HTTP_404_NOT_FOUND)
        
    permission_classes = [IsAuthenticated]
    def delete(self, request, project_id, user_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            membership = Membership.objects.filter(project=project, user__id=user_id)
            membership.delete()
            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success" }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found" }, status=status.HTTP_404_NOT_FOUND)
        
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        user = request.user
        serializer = UpdateRoleSerializer(data=request.data)
        if serializer.is_valid():
            userId = request.data.get("userId")
            projectId = request.data.get("projectId")
            role = request.data.get("role")

            membership = Membership.objects.get(project__id=projectId, user__id=userId)
            if membership is not None:
                membership.role = role
                membership.save()
                serialized_membership = MembershipSerializer(membership).data
                return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_membership }, status=status.HTTP_200_OK)
            else:
                return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'User is not found in project' }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)


class TeamMember(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            memberships = Membership.objects.filter(project=project)
            serialized_membership = TeamMemberSerializer(memberships, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_membership }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found" }, status=status.HTTP_404_NOT_FOUND)