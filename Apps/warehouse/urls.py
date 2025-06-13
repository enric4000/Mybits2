from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.WarehouseCreateView.as_view(), name="warehouse-create"),
    path("<uuid:pk>/participant/", views.WarehouseLuggageByParticipantView.as_view(), name="luggage-list"),
    path("<uuid:pk>/participant/<uuid:participant_id>/create/", views.WarehouseLuggageCreateView.as_view(), name="luggage-create"),
    path("<uuid:pk>/participant/<uuid:participant_id>/", views.WarehouseLuggageByParticipantView.as_view(), name="luggage-create"),
    path("<uuid:pk>/luggage/<uuid:luggage_id>/", views.WarehouseLuggageCRUDView.as_view(), name="luggage-list"),
    path("<uuid:pk>/luggage/", views.WarehouseLuggageView.as_view(), name="luggage-list"),
    path("<uuid:pk>/", views.WarehouseCRUDView.as_view(), name="warehouse-detail"),
    path("", views.WarehouseView.as_view(), name="warehouse-list"),
]