from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

from user.models import User

class Contact(models.Model):
    user = models.ForeignKey(User, related_name='friends', on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"Contact: {self.user} ({self.pk})"
    
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message: {self.contact.user} ({self.content})"
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
class Chat(models.Model):
    participants = models.ManyToManyField(Contact, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True) 
    
    def __str__(self):
        return "{}".format(self.pk)
