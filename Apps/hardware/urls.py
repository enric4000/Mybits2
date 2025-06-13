from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.HardwareItemCreateView.as_view(), name="hardware-create"),
    path("<uuid:pk>/borrow/", views.HardwareItemBorrowView.as_view(), name="hardware-borrow"),
    path("<uuid:pk>/return/", views.HardwareItemReturnView.as_view(), name="hardware-return"),
    path("<uuid:pk>/", views.HardwareItemCRUDView.as_view(), name="hardware-detail"),
    path("", views.HardwareItemView.as_view(), name="hardware-list"),
]
