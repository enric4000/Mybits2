from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.EventCreationView.as_view(), name='event-create'),
    path('<uuid:pk>/', views.EventCRUDView.as_view(), name='event-detail'),
    path('', views.EventView.as_view(), name='event'),
]
