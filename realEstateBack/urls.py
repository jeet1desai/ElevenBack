from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/user/', include("user.urls")),
    path('api/v1/project/', include("project.urls")),
    path('api/v1/teams/', include("team.urls")),
]
