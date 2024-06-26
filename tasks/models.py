from django.db import models
from realEstateBack.choice import TASK_STATUS_CHOICES
from user.models import User
from project.models import Project
from django.utils import timezone

class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    status = models.PositiveSmallIntegerField(choices=TASK_STATUS_CHOICES, default=1)
    address = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    assign = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_by_task')
    modified_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_by_task')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"
    

class TaskComment(models.Model):
    id = models.AutoField(primary_key=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=1000, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_by_task_comment')

    def __str__(self):
        return f"URL for {self.task.title}: {self.comment}"

