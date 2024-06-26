from django.urls import path
from . import views

urlpatterns = [
    path('team/<int:project_id>', views.Teams.as_view(), name="get team list"),
    path('team/<int:project_id>/<int:user_id>', views.Teams.as_view(), name="remove team member"),
    path('team', views.Teams.as_view(), name="update team member role"),

    # Util
    path('team/member/<int:project_id>', views.TeamMember.as_view(), name="get team member"),
]