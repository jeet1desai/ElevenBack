from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Chat, Contact
from rest_framework import status
from rest_framework.exceptions import ValidationError
from user.models import User

def get_user_contact(id):
    user = get_object_or_404(User, id=id)
    return get_object_or_404(Contact, user=user)


class ContactSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value

class ChatSerializer(serializers.ModelSerializer):
    participants= ContactSerializer(many=True)

    class Meta:
        model= Chat
        fields= ('id', 'messages', 'participants')

    def create(self, validated_data):

        participants= validated_data.pop('participants')
        contacts= []
        for id in participants:
            contact= get_user_contact(id)
            contacts.append(contact)

        if participants[0]==participants[1]:
            raise ValidationError({'error': 'No place for loners :('}, code=status.HTTP_406_NOT_ACCEPTABLE)

        chat= Chat.objects.filter(participants=contacts[0]) & Chat.objects.filter(participants=contacts[1])
        chat= chat.first()

        if chat is not None:
            raise ValidationError({'error': 'Chat already exists'}, code=status.HTTP_406_NOT_ACCEPTABLE)
        
        chat = Chat.objects.create()

        for id in participants:
            contact= get_user_contact(id)
            chat.participants.add(contact)

        chat.save()
        return chat