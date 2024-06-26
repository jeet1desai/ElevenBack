from django.urls import path
from . import views

urlpatterns = [
    path('calender', views.CalenderMethod.as_view(), name="create calender"),
    path('calender/<int:calender_id>', views.CalenderMethod.as_view(), name="edit, delete calendar"),
    path('calender/project/<int:project_id>', views.CalenderEvents.as_view(), name="get all events"),
    path('calender/comment/<int:calender_id>', views.CalenderComments.as_view(), name="get and add comment"),
]