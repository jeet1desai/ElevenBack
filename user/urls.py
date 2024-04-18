from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('invite/', views.Invite.as_view(), name="invite"),
]