from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView)
from .serializers import ChatSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404
from .models import Chat, Contact
from user.models import User
from rest_framework import status
from rest_framework.response import Response


def last_15_messages(chatID):
    chat= get_object_or_404(Chat, id=chatID)
    return chat.messages.order_by('-timestamp').all()


def get_user_contact(id):
    user= get_object_or_404(User, id=id)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatID):
    return get_object_or_404(Chat, id=chatID)


class ChatListView(ListAPIView):
    queryset = Chat.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        queryset = Chat.objects.all()
        if user is not None:
            user = get_object_or_404(User, id=user.id)
            contact = get_object_or_404(Contact, user=user)

            queryset = contact.chats.all()

            serializer_class = ChatSerializer(queryset, many=True).data
            return Response({ 'status': status.HTTP_200_OK, 'msg': "Success", 'data': serializer_class }, status=status.HTTP_200_OK)
        else:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Something went wrong' }, status=status.HTTP_400_BAD_REQUEST)


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


class ChatDetailView(RetrieveAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


class ChatUpdateView(UpdateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]


class ChatDeleteView(DestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
