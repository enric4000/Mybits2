from django.conf import settings

from Apps.event.services import EventService
from Apps.participant.services import ParticipantService


def globalContext(request):
    baseUrl = (settings.BASE_URL if hasattr(settings, "BASE_URL") else "http://localhost:8000")

    if("/event/" in request.path and len(request.path) > 43):
        event_id = request.path.split("/")[2]
        extend_navigation = True
        try:
            event = EventService.get_event(event_id)

        except Exception as e:
            is_admin = False
            activities_enabled = False
            hardware_enabled = False
            warehouse_enabled = False
            judging_enabled = False

        if ParticipantService.is_user_admin(event, request.user):
            is_admin = True
            activities_enabled = event.activities_enabled
            hardware_enabled = event.hardware_enabled
            warehouse_enabled = event.warehouse_enabled
            judging_enabled = event.judging_enabled
        
        else:
            is_admin = False
            activities_enabled = False
            hardware_enabled = event.hardware_enabled
            warehouse_enabled = False
            judging_enabled = False
    
    else:
        extend_navigation = False
        is_admin = False
        activities_enabled = False
        hardware_enabled = False
        warehouse_enabled = False
        judging_enabled = False

    return {
        "baseUrl": baseUrl,
        "app_name": "Mybits2",
        "app_author": "Hackers@UPC",
        "app_description": "This Mybits2, a hackathon and/or event manager!",
        "organization": "Hackers@UPC",
        "organization_url": "https://hackers",
        "organization_contact": "contact@hackupc.com",
        "mediaLinks": {
            "facebook": "https://www.facebook.com/hackupc",
            "twitter": "https://x.com/hackupc",
            "instagram": "https://www.instagram.com/hackupc/",
            "linkedin": "https://www.linkedin.com/company/hackupc",
            "medium": "https://medium.com/@hackupc",
            "github": "htps://github.com/hackupc",
            "youtube": "https://www.youtube.com/channel/UCiiRorGg59Xd5Sjj9bjIt-g",
            "mail": "mailto:contact@hackupc.com",
        },
        "login": baseUrl + "/user/login/",
        "profile": baseUrl + "/user/profile/",
        "logout": baseUrl + "/user/logout/",
        "register": baseUrl + "/user/register/",
        "password_reset": baseUrl + "/password/reset/",
        "extend_navigation": extend_navigation,
        "is_admin": is_admin,
        "activities_enabled": activities_enabled,
        "hardware_enabled": hardware_enabled,
        "warehouse_enabled": warehouse_enabled,
        "judging_enabled": judging_enabled,
    }

def path_length(request):
    return {
        'path_length': len(request.path) if request and request.path else 0
    }