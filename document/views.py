from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CreateDocumentSerializer, DocumentSerializer, DeleteDocumentSerializer, PublishDocumentSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Document
from user.models import User
from project.models import Project
from django.utils import timezone

class CreateDocument(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        serializer = CreateDocumentSerializer(data=request.data)
        if serializer.is_valid():
            userId = request.data.get('userId')
            projectId = request.data.get('projectId')
            name = request.data.get('name')
            url = request.data.get('url')
            is_published = request.data.get('is_published')

            user_instance = User.objects.get(id=userId, is_active=True)
            project_instance = Project.objects.get(id=projectId, is_active=True)
            document_instance = Document.objects.create(
                user=user_instance, project=project_instance, name=name, url=url, is_published=is_published, modified_by=user_instance, modified_date=timezone.now()
            )
            serialized_documents = DocumentSerializer(document_instance).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_documents }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)


class TeamDocument(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            documents = Document.objects.filter(project=project, is_published=True, is_active=True)
            serialized_documents = DocumentSerializer(documents, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_documents }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Project not found' }, status=status.HTTP_400_BAD_REQUEST)

 
class MyDocument(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, project_id, format=None):
        user = request.user
        try:
            project = Project.objects.get(id=project_id, is_active=True)
            documents = Document.objects.filter(project=project, is_active=True)
            serialized_documents = DocumentSerializer(documents, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_documents }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Project not found' }, status=status.HTTP_400_BAD_REQUEST)


class DeleteDocument(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        user = request.user
        serializer = DeleteDocumentSerializer(data=request.data)
        if serializer.is_valid():
            docId = request.data.get('docId')
            role = request.data.get('role')
            projectId = request.data.get('projectId')

            document = Document.objects.get(id=docId, project__id=projectId, is_active=True)
            if document.is_published == False:
                document.is_active = False
                document.modified_by = user
                document.modified_date = timezone.now()
                document.save()
                serialized_documents = DocumentSerializer(document).data
                return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_documents }, status=status.HTTP_200_OK)
            else:
                if role == 3 or role == 4:
                    document.is_active = False
                    document.modified_by = user
                    document.modified_date = timezone.now()
                    document.save()
                    serialized_documents = DocumentSerializer(document).data
                    return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_documents }, status=status.HTTP_200_OK)
                else:
                    return Response({ 'status': status.HTTP_200_OK, 'msg': 'You are not authorized' }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)


class PublishDocument(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, format=None):
        user = request.user
        serializer = DeleteDocumentSerializer(data=request.data)
        if serializer.is_valid():
            docId = request.data.get('docId')
            role = request.data.get('role')
            projectId = request.data.get('projectId')
            isPublish = request.data.get('isPublish')

            document = Document.objects.get(id=docId, project__id=projectId, is_active=True)
            if isPublish == False:
                if role == 3 or role == 4:
                    document.is_published = False
                    document.modified_by = user
                    document.modified_date = timezone.now()
                    document.save()
                    serialized_documents = DocumentSerializer(document).data
                    return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_documents }, status=status.HTTP_200_OK)
                else:
                    return Response({ 'status': status.HTTP_200_OK, 'msg': 'You are not authorized' }, status=status.HTTP_200_OK)
            else:
                if role == 2 or role == 3 or role == 4:
                    document.is_published = False
                    document.modified_by = user
                    document.modified_date = timezone.now()
                    document.save()
                    serialized_documents = DocumentSerializer(document).data
                    return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_documents }, status=status.HTTP_200_OK)
                else:
                    return Response({ 'status': status.HTTP_200_OK, 'msg': 'You are not authorized' }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)
