from django.urls import path
from . import views

urlpatterns = [
    path('task', views.Tasks.as_view(), name="create task"),
    path('task/<int:task_id>', views.Tasks.as_view(), name="edit, delete and get task"),
]