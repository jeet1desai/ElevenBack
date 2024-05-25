from django.contrib import admin
from .models import Calender, CalenderComment

@admin.register(Calender)
class CalenderModel(admin.ModelAdmin):
  list_display = ("id", "title", "project", "is_active")

@admin.register(CalenderComment)
class CalenderCommentModel(admin.ModelAdmin):
  list_display = ("id", "comment", "comment", "created_by")
