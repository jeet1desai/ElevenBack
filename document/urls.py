from django.urls import path
from . import views

urlpatterns = [
   path('document', views.CreateDocument.as_view(), name="create document"),
   path('team/<int:project_id>', views.TeamDocument.as_view(), name="get team document"),
   path('my/<int:project_id>', views.MyDocument.as_view(), name="get my document"),
   path('delete', views.DeleteDocument.as_view(), name="delete document"),
   path('publish', views.PublishDocument.as_view(), name="publish / un publish document"),
]