from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, InviteSerializer, UserSerializer
from project.serializers import ProjectSerializer
from .models import User
from project.models import Project, Membership
import random
import string
from django.utils import timezone
from realEstateBack import utils

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class Login(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email_value = serializer.data.get("email")
            user = User.objects.get(email=email_value)
            serialized_user = UserSerializer(user).data

            token = get_tokens_for_user(user)

            memberships = Membership.objects.filter(user=user)
            if memberships.exists():
                projects = [membership.project for membership in memberships]
                serialized_projects = ProjectSerializer(projects, many=True).data
                return Response({ 'status': status.HTTP_200_OK, 'msg': "Successfully login", 'data': { 'user': serialized_user, 'projects': serialized_projects }, 'token': token }, status=status.HTTP_200_OK)
            else:
                return Response({ 'status': status.HTTP_400_BAD_REQUEST, "error": "User is not associated with any projects" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        
class Invite(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = InviteSerializer(data=request.data)

        id = request.data.get('projectId')
        email = request.data.get('email')
        role = request.data.get('role')
        user = request.user

        if serializer.is_valid():
            try:
                project = Project.objects.get(id=id)
            except Project.DoesNotExist:
                return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                iUser = User.objects.get(email=email)
                utils.send_invitation_mail(email, project.name)
            except User.DoesNotExist:
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
                iUser = User.objects.create_user(email=email, password=password, created_by=user, modified_by=user, created_date=timezone.now(), modified_date=timezone.now())
                utils.send_welcome_mail(email, password, project.name)

            Membership.objects.create(user=iUser, project=project, role=role)

            return Response({ 'status': status.HTTP_200_OK, 'msg': "User invited successfully" } , status=status.HTTP_201_CREATED)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
            
            

