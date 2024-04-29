from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentModel(admin.ModelAdmin):
    list_display = ("id", "user", "project", "name", "is_published", "is_active")
