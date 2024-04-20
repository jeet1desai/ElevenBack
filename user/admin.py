from django.contrib import admin
from .models import User, Company

# Register your models here.
# admin.site.register(User)
@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "is_active")

@admin.register(Company)
class CompanyModel(admin.ModelAdmin):
    list_display = ("id", "company", "user")