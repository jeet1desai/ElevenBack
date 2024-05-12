from django.urls import path

from .views import (
    ChatListView, ChatCreateView, ChatDetailView, ChatUpdateView, ChatDeleteView, CreateContactView
)

urlpatterns = [
  path('chat', ChatListView.as_view()),
  path('chat/create', ChatCreateView.as_view()),
  path('chat/<pk>', ChatDetailView.as_view()),
  path('chat/<pk>/update', ChatUpdateView.as_view()),
  path('chat/<pk>/delete', ChatDeleteView.as_view()),
  path('chat/create-contact', CreateContactView.as_view()),
]