from django.urls import path
from . import views

urlpatterns = [
    path('projects', views.Projects.as_view(), name="get projects"),
]