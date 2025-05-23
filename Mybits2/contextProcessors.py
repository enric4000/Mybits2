from django.conf import settings


def globalContext(request):
    baseUrl = (settings.BASE_URL if hasattr(settings, "BASE_URL") else "http://localhost:8000")
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
        "login": baseUrl + "/user/login",
        "profile": baseUrl + "/user/profile",
        "logout": baseUrl + "/user/logout",
        "register": baseUrl + "/user/register",
        "password_reset": baseUrl + "/password/reset",
    }
