from enum import Enum


class ParticipantTypeEnum(Enum):
    """
    Enum representing the types of participants.
    """

    HACKER = "Hacker"
    MENTOR = "Mentor"
    VOLUNTEER = "Volunteer"
    SPONSOR = "Sponsor"
    ADMIN = "Admin"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples containing the enum name and value.
        """
        return [(tag.name, tag.value) for tag in cls]
