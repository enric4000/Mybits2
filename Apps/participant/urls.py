from django.urls import path
from . import views

urlpatterns = [
    path("apply/", views.ParticipantApplicationView.as_view(), name="event-create"),
    path("<uuid:pk>/", views.ParticipantCRUDView.as_view(), name="event-detail"),
    path("", views.ParticipantView.as_view(), name="event"),
]
