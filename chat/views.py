from rest_framework.generics import (ListAPIView, CreateAPIView)
from .serializers import ChatSerializer
from rest_framework import permissions
from django.shortcuts import render, get_object_or_404
from .models import Chat, Contact
from user.models import User


def last_15_messages(chatID):
    chat= get_object_or_404(Chat, id=chatID)
    return chat.messages.order_by('-timestamp').all()


def get_user_contact(id):
    user= get_object_or_404(User, id=id)
    return get_object_or_404(Contact, user=user)


def get_current_chat(chatID):
    return get_object_or_404(Chat, id=chatID)


class ChatListView(ListAPIView):
    serializer_class= ChatSerializer
    permission_classes= [permissions.AllowAny, ]

    def get_queryset(self):
        queryset= Chat.objects.all()
        id= self.request.query_params.get('id', None)

        if id is not None:
            user= get_object_or_404(User, id=id)
            contact= get_object_or_404(Contact, user=user)

            queryset= contact.chats.all()
        
        return queryset


class ChatCreateView(CreateAPIView):
    queryset= Chat.objects.all()
    serializer_class= ChatSerializer
    permission_classes= [permissions.IsAuthenticated, ]