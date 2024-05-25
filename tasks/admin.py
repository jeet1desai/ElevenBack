from django.contrib import admin
from .models import Task, TaskComment

@admin.register(Task)
class TaskModel(admin.ModelAdmin):
    list_display = ("id", "title", "project", "status", "is_active")

@admin.register(TaskComment)
class TaskCommentModel(admin.ModelAdmin):
    list_display = ("id", "task", "comment", "created_by")