from django.db import models
from user.models import User
from project.models import Project
from django.utils import timezone

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    url = models.CharField(max_length=500, null=False)
    type = models.CharField(max_length=10, null=False, default="")
    name = models.CharField(max_length=50, null=False)
    is_published = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    modified_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_by_document')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
