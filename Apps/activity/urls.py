from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.ActivityCreateView.as_view(), name="activity-create"),
    path("<uuid:pk>/checkin/", views.ActivityCheckinView.as_view(), name="activity-join"),
    path("<uuid:pk>/", views.ActivityCRUDView.as_view(), name="activity-detail"),
    path("", views.ActivityView.as_view(), name="activity-list"),
]