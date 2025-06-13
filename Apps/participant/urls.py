from django.urls import path
from . import views

urlpatterns = [
    path(
        "apply/", views.ParticipantApplicationView.as_view(), name="participant-apply"
    ),
    path(
        "checkin/", views.ParticipantCheckInView.as_view(), name="participant-checkin"
    ),
    path("mine/", views.ParticipantMineView.as_view(), name="participant-Mine"),
    path("id/", views.ParticipantMineIdView.as_view(), name="participant-id"),
    path("<uuid:pk>/id/", views.ParticipantIdView.as_view(), name="participant-id"),
    path("<uuid:pk>/accept/", views.ParticipantAcceptView.as_view(), name="participant-accept"),
    path("<uuid:pk>/reject/", views.ParticipantRejectView.as_view(), name="participant-reject"),
    path("<uuid:pk>/", views.ParticipantCRUDView.as_view(), name="participant-detail"),
    path("", views.ParticipantView.as_view(), name="participant-list"),
]
