from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    
class User(AbstractUser):
    GENDER_CHOICES = (
        (1, 'Male'),
        (2, 'Female'),
        (3, 'Other'),
    )

    COUNTRY_CHOICES = (
        ('+91', 'IN'),  
        ('+1', 'USA'),   
        ('+2', 'CAN'),
    )

    username = None
    groups = None
    last_login = None
    date_joined = None
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, default=1)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    country_code = models.CharField(max_length=10, choices=COUNTRY_CHOICES, default='+91')
    profile_picture = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_by_set')
    modified_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    modified_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_by_set')
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"