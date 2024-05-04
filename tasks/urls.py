from django.urls import path
from . import views

urlpatterns = [
    path('task', views.Tasks.as_view(), name="create task"),
    path('task/<int:task_id>', views.Tasks.as_view(), name="edit, delete and get task"),
    path('team/<int:project_id>', views.GetTeamTasks.as_view(), name="get team task"),
    path('my/<int:project_id>', views.GetMyTasks.as_view(), name="get my task"),
]