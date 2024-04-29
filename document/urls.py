from django.urls import path
from . import views

urlpatterns = [
   path('team', views.TeamDocument.as_view(), name="get team document"),
   path('my', views.TeamDocument.as_view(), name="get team document"),
]