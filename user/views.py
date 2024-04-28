from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, InviteSerializer, UserSerializer, UserProfileUpdateSerializer, CompanySerializer
from .models import User, Company
from project.models import Project, Membership
import random
import string
from django.utils import timezone
from realEstateBack import utils
from project.views import get_serialized_projects
from django.contrib.auth import authenticate

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
            email_value = request.data.get("email")
            pass_value = serializer.data.get("password")
            user = authenticate(request, email=email_value, password=pass_value)

            if user is None:
                return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Please enter valid credential'}, status=status.HTTP_400_BAD_REQUEST)

            serialized_user = UserSerializer(user).data

            token = get_tokens_for_user(user)

            if user.is_superuser:
                try:
                    Company.objects.get(user=user)
                except Company.DoesNotExist:
                    memberships = Membership.objects.filter(user=user)
                    if memberships.exists():
                        projects = [membership.project for membership in memberships]
                        serialized_projects = get_serialized_projects(self, projects, user)
                        return Response({ 'status': status.HTTP_200_OK, 'msg': "Successfully login", 'user': serialized_user, 'projects': serialized_projects, 'is_company': False, 'token': token }, status=status.HTTP_200_OK)
                    else:
                        return Response({ 'status': status.HTTP_200_OK, 'msg': "Successfully login", 'user': serialized_user, 'projects': [], 'is_company': False, 'token': token }, status=status.HTTP_200_OK)
            
            memberships = Membership.objects.filter(user=user)
            if memberships.exists():
                projects = [membership.project for membership in memberships]
                serialized_projects = get_serialized_projects(self, projects, user)
                return Response({ 'status': status.HTTP_200_OK, 'msg': "Successfully login", 'user': serialized_user, 'projects': serialized_projects, 'is_company': True, 'token': token }, status=status.HTTP_200_OK)
            else:
                return Response({ 'status': status.HTTP_400_BAD_REQUEST, "error": "User is not associated with any projects" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)


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

            memberships = Membership.objects.filter(user=iUser, project=project)
            if not memberships.exists():
                Membership.objects.create(user=iUser, project=project, role=role, modified_date=timezone.now(), modified_by=user)
                return Response({ 'status': status.HTTP_200_OK, 'msg': "User invited successfully" } , status=status.HTTP_200_OK)
            else:
                return Response({ 'status': status.HTTP_200_OK, 'msg': "User is already part of the project" } , status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': "Something went wrong" }, status=status.HTTP_400_BAD_REQUEST)
    
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
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

            iUser = User.objects.get(email=email)

            memberships = Membership.objects.get(user=iUser, project=project)
            memberships.role = role
            memberships.modified_date = timezone.now()
            memberships.modified_by = user
            memberships.save()
            return Response({ 'status': status.HTTP_200_OK, 'msg': "User role is updated" } , status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class Profile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        try:
            user = User.objects.get(id=request.user.id)
            serialized_user = UserSerializer(user).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_user }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "User not found" }, status=status.HTTP_404_NOT_FOUND)
        
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserProfileUpdateSerializer(user, data=request.data)
            if serializer.is_valid():
                user.modified_date = timezone.now()
                user.modified_by = user
                user.gender = request.data.get('gender')
                user.phone_number = request.data.get('phone_number')
                user.country_code = request.data.get('country_code')
                user.profile_picture = request.data.get('profile_picture')
                user.address = request.data.get('address')
                user.save()

                serialized_user = UserSerializer(user).data
                return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_user }, status=status.HTTP_200_OK)
            else:
               return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "User not found" }, status=status.HTTP_404_NOT_FOUND)


class CompanyView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        serializer = CompanySerializer(data=request.data, context={'user':user})
        if serializer.is_valid():
            title = request.data.get('title')
            company = request.data.get('company')
            type = request.data.get('type')
            industry = request.data.get('industry')
            country_code = request.data.get('country_code')
            phone_number = request.data.get('phone_number')
            company_instance = Company.objects.create(
                user=user, title=title, company=company, type=type, industry=industry, country_code=country_code, phone_number=phone_number
            )
            serialized_company = CompanySerializer(company_instance).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': "Company created successfully", "company": serialized_company }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': "Something went wrong" }, status=status.HTTP_400_BAD_REQUEST)


class MeUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        try:
            user_data = User.objects.get(id=user.id)
            serialized_user = UserSerializer(user_data).data
            token = get_tokens_for_user(user_data)

            if user_data.is_superuser:
                try:
                    company = Company.objects.get(user=user_data)
                    return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'user': serialized_user, 'is_company': True, 'token': token }, status=status.HTTP_200_OK)
                except Company.DoesNotExist:
                    return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'user': serialized_user, 'is_company': False, 'token': token }, status=status.HTTP_200_OK)
            else:
                return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'user': serialized_user, 'is_company': True, 'token': token }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "User not found" }, status=status.HTTP_404_NOT_FOUND)
