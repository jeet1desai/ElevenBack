from django.urls import path
from . import views

urlpatterns = [
    path('calender', views.Calender.as_view(), name="create calender"),
]