from Apps.users import views
from django.urls import path

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("register/", views.CustomRegisterView.as_view(), name="register"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("<pk>/profile/", views.UserProfileView.as_view(), name="user-profile"),
    path("", views.UsersView.as_view(), name="users"),
]
