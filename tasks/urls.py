from django.urls import path
from . import views

urlpatterns = [
    path('task', views.Tasks.as_view(), name="create tasks"),
]