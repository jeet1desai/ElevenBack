from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('invite/', views.Invite.as_view(), name="invite"),

    path('profile/', views.Profile.as_view(), name="get profile"),
    path('update_user/', views.Profile.as_view(), name="update user"),
]