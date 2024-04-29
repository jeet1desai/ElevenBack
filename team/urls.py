from django.urls import path
from . import views

urlpatterns = [
    path('team/<int:project_id>', views.Teams.as_view(), name="get team list"),
    path('team/<int:project_id>/<int:user_id>', views.Teams.as_view(), name="remove team member"),
]