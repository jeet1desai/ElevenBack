from django.contrib import admin
from .models import User

# Register your models here.
# admin.site.register(User)
@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "is_active")