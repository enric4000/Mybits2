from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.ProjectCreateView.as_view(), name="project-create"),
    path("<uuid:pk>/valorate/", views.ProjectValorationView.as_view(), name="valoration-create"),
    path("<uuid:pk>/", views.ProjectCRUDView.as_view(), name="project-detail"),
    path("", views.ProjectView.as_view(), name="project-list"),
]