"""
URL configuration for Mybits2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.HomeView.as_view(), name="home"),
    path("user/", include("Apps.users.urls")),
    path("event/<str:event_id>/participant/", include("Apps.participant.urls")),
    path("event/<str:event_id>/team/", include("Apps.team.urls")),
    path("event/<str:event_id>/activity/", include("Apps.activity.urls")),
    path("event/<str:event_id>/hardware/", include("Apps.hardware.urls")),
    path("event/<str:event_id>/warehouse/", include("Apps.warehouse.urls")),
    path("event/<str:event_id>/project/", include("Apps.project.urls")),
    path("event/", include("Apps.event.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
