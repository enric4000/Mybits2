from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.TeamCreateView.as_view(), name="team-create"),
    path("join/", views.TeamJoinView.as_view(), name="team-join"),
    path("id/", views.TeamIdView.as_view(), name="team-id"),
    path("<uuid:pk>/id/", views.TeamIdView.as_view(), name="team-id"),
    path("<uuid:pk>/", views.TeamCRUDView.as_view(), name="team-detail"),
    path("", views.TeamView.as_view(), name="team-list"),
]
