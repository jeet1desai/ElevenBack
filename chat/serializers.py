from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Chat, Contact, Message
from rest_framework import status
from rest_framework.exceptions import ValidationError
from user.models import User
from user.serializers import UserSerializer


def get_user_contact(id):
    user = get_object_or_404(User, id=id)
    return get_object_or_404(Contact, user=user)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data
        representation['friends'] = UserSerializer(instance.friends, many=True).data
        return representation
    

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['contact'] = ContactSerializer(instance.contact).data
        return representation


class ParticipantsSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value
    
class ChatSerializer(serializers.ModelSerializer):
    participants = ParticipantsSerializer(many=True)

    class Meta:
        model= Chat
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['participants'] = ContactSerializer(instance.participants, many=True).data
        representation['messages'] = MessageSerializer(instance.messages, many=True).data
        return representation

    def create(self, validated_data):
        participants = validated_data.pop('participants')
        contacts = []
        for id in participants:
            contact = get_user_contact(id)
            contacts.append(contact)

        if participants[0] == participants[1]:
            raise ValidationError({'msg': 'No place for loners :('}, code=status.HTTP_400_BAD_REQUEST)

        chat = Chat.objects.filter(participants=contacts[0]) & Chat.objects.filter(participants=contacts[1])
        chat = chat.first()

        if chat is not None:
            raise ValidationError({'msg': 'Chat already exists'}, code=status.HTTP_400_BAD_REQUEST)
        
        chat = Chat.objects.create()

        for id in participants:
            contact = get_user_contact(id)
            chat.participants.add(contact)

        chat.save()
        return chat