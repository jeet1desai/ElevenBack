from django.db import models
from user.models import User
from django.utils import timezone
from project.models import Project

class Calender(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    color = models.CharField(max_length=100, null=True, blank=True)
    background_color = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    assign = models.ManyToManyField(User, related_name='assigned_calenders', blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_by_calender')
    modified_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_by_calender')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"


class CalenderComment(models.Model):
    id = models.AutoField(primary_key=True)
    calender = models.ForeignKey(Calender, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=1000, null=False)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_by_calender_comment')

    def __str__(self):
        return f"{self.calender.title}: {self.comment}"
