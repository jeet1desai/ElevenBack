from django.contrib import admin
from .models import Project, Membership

@admin.register(Project)
class ProjectModel(admin.ModelAdmin):
    list_display = ("id", "name", "code", "status", "is_active")


@admin.register(Membership)
class MembershipModel(admin.ModelAdmin):
    list_display = ("id", "user", "project", "role")
