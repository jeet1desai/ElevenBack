from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Membership, Project
from user.models import User, Company
from .serializers import ProjectSerializer, CreateProjectSerializer
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime

def get_serialized_projects(self, projects, user):
    serialized_projects = []
    for project in projects:
        memberships = Membership.objects.filter(project=project)

        unique_users = memberships.values_list('user', flat=True).distinct()
        user_count = len(unique_users)

        membership = memberships.filter(user=user).first()
        user_role = membership.role if membership else None
        
        project_data = ProjectSerializer(project).data
        project_data['user_role'] = user_role
        project_data['user_count'] = user_count
        
        serialized_projects.append(project_data)

    return serialized_projects

class Projects(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        memberships = Membership.objects.filter(user=user)
        if memberships.exists():
            projects = [membership.project for membership in memberships]
            serialized_projects = get_serialized_projects(self, projects, user)
            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_projects }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found" }, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        serializer = CreateProjectSerializer(data=request.data)
        if serializer.is_valid():
            name = request.data.get('name')
            code = request.data.get('code')
            address = request.data.get('address')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            p_status =  request.data.get('status')

            if user.is_superuser:
                project = Project(
                    name=name, code=code, status=p_status, address=address,
                    start_date=datetime.strptime(start_date, '%Y-%m-%d') if start_date else None,
                    end_date=datetime.strptime(end_date, '%Y-%m-%d') if end_date else None,
                    created_date=timezone.now(), created_by=user,
                    modified_date=timezone.now(), modified_by=user
                )
                project.save()

                company = Company.objects.get(user=user)
                if company is None:
                    return Response({ 'status': status.HTTP_400_BAD_REQUEST, "error": "Please provide company detail first" }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    membership = Membership.objects.create(user=user, project=project, role=4, company=company, modified_date=timezone.now(), modified_by=user)
                    memberships = Membership.objects.filter(project=project)
                    user_role = membership.role if membership else None
                    unique_users = memberships.values_list('user', flat=True).distinct()
                    user_count = len(unique_users)

                    serialized_projects = ProjectSerializer(project).data
                    serialized_projects['user_role'] = user_role
                    serialized_projects['user_count'] = user_count
                    return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_projects }, status=status.HTTP_200_OK)
            else:
                return Response({ 'status': status.HTTP_400_BAD_REQUEST, "error": "User is not authorized" }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)


class ProjectsDetails(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id)
            serialized_project_detail = ProjectSerializer(project).data

            memberships = Membership.objects.filter(project=project)
            membership = memberships.filter(user=user).first()
            user_role = membership.role if membership else None
            serialized_project_detail['user_role'] = user_role

            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_project_detail }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found" }, status=status.HTTP_404_NOT_FOUND)

    permission_classes = [IsAuthenticated]
    def put(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            serializer = CreateProjectSerializer(project, data=request.data)
            if serializer.is_valid():
                start_date = request.data.get('start_date')
                end_date = request.data.get('end_date')

                project.name = request.data.get('name')
                project.code = request.data.get('code')
                project.address = request.data.get('address')
                project.status =  request.data.get('status')
                project.modified_date = timezone.now()
                project.modified_by = user
                if start_date:
                    project.start_date = datetime.strptime(start_date, '%Y-%m-%d')
                else:
                    project.start_date = None
                if end_date:
                    project.end_date = datetime.strptime(end_date, '%Y-%m-%d')
                else:
                    project.end_date = None
                project.save()

                serialized_project_detail = ProjectSerializer(project).data

                memberships = Membership.objects.filter(project=project)
                membership = memberships.filter(user=user).first()
                user_role = membership.role if membership else None
                serialized_project_detail['user_role'] = user_role

                return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serialized_project_detail }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_404_NOT_FOUND, 'msg': "Project not found" }, status=status.HTTP_404_NOT_FOUND)

