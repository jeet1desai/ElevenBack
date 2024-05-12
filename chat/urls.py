from django.urls import path

from .views import (
  ChatListView, ChatCreateView, ChatDetailView, ChatUpdateView, ChatDeleteView
)

urlpatterns = [
  path('chat/list', ChatListView.as_view()),
  path('chat/create', ChatCreateView.as_view()),
  path('chat/<pk>', ChatDetailView.as_view()),
  path('chat/<pk>/update', ChatUpdateView.as_view()),
  path('chat/<pk>/delete', ChatDeleteView.as_view()),
]