from rest_framework.generics import (CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView)
from rest_framework.views import APIView
from .serializers import ChatSerializer
from rest_framework import permissions
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


class ChatListView(APIView):
    def get(self, request, format=None):
        user = request.user
        try:
            contact = Contact.objects.get(user=user)
            friends = contact.friends.all()
            print('friends => ', friends)

            serialized_chats = []
            for friend in friends:
                friend_contact = Contact.objects.get(user=friend)
                print(friend_contact)
                chat = Chat.objects.filter(participants=contact).filter(participants=friend_contact)
                chat_data = ChatSerializer(chat, many=True).data
                serialized_chats.extend(chat_data)
            return Response({ 'status': status.HTTP_200_OK, 'msg': 'Success', 'data': serialized_chats }, status=status.HTTP_200_OK)
        except Contact.DoesNotExist:
            return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Contact not found' }, status=status.HTTP_400_BAD_REQUEST)


class ChatCreateView(CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes= [permissions.IsAuthenticated]


class ChatDetailView(RetrieveAPIView):
    queryset= Chat.objects.all()
    serializer_class= ChatSerializer
    permission_classes= [permissions.AllowAny, ]

class ChatUpdateView(UpdateAPIView):
    queryset= Chat.objects.all()
    serializer_class= ChatSerializer
    permission_classes= [permissions.IsAuthenticated, ]

class ChatDeleteView(DestroyAPIView):
    queryset= Chat.objects.all()
    serializer_class= ChatSerializer
    permission_classes= [permissions.IsAuthenticated, ]


class CreateContactView(DestroyAPIView):
    def post(self, request, format=None):
        friend_id = request.data.get('friend_id')
        user = request.user
        friend = get_object_or_404(User, id=friend_id)

        contact, created = Contact.objects.get_or_create(user=user)

        if created:
           contact.friends.add(friend)
           return Response({ 'status': status.HTTP_201_CREATED, 'msg': 'Contact created successfully' }, status=status.HTTP_201_CREATED)
        else:
            if friend in contact.friends.all():
                return Response({ 'status': status.HTTP_400_BAD_REQUEST, 'msg': 'Friend already added' }, status=status.HTTP_400_BAD_REQUEST)
            else:
                contact.friends.add(friend)
                return Response({ 'status': status.HTTP_200_OK, 'msg': 'Friend added to contact' }, status=status.HTTP_200_OK)