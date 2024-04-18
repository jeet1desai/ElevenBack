from django.db import models
from user.models import User
from django.utils import timezone

class Project(models.Model):
    STATUS_CHOICES = (
        (1, 'In Progress'),
        (2, 'Active'),
        (3, 'Construction'),
        (4, 'Pre Construction'),
        (5, 'Bidding'),
        (6, 'Complete'),
        (7, 'Other'),
        (8, 'None'),
    )

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    code = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_by_project')
    modified_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_by_project')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
    

class Membership(models.Model):
    ROLE_CHOICES = (
        (1, 'Collaborator'),
        (2, 'Power Collaborator'),
        (3, 'Admin'),
    )

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=1)

    def __str__(self):
        return f"{self.user} {self.project}"