from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login.as_view(), name="login"),
    path('change-password', views.ChangePassword.as_view(), name='change password'),
    path('invite', views.Invite.as_view(), name="invite member"),
    path('me', views.MeUser.as_view(), name="invite member"),
    path('delete', views.DeleteUser.as_view(), name="delete user"),

    path('profile', views.Profile.as_view(), name="get profile"),
    path('update_user', views.Profile.as_view(), name="update user"),

    path('company', views.CompanyView.as_view(), name="create company"),
    path('company/<int:company_id>', views.CompanyView.as_view(), name="get company"),

    path('stats/<int:project_id>', views.StatsView.as_view(), name="get dash stats"),
]