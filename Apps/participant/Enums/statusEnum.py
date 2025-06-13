from enum import Enum

class StatusEnum(Enum):
    """
    Enum representing the status of a participant.
    """
    UNDER_REVIEW = "Under Review"
    CANCELLED = "Cancelled"
    INVITED = "Invited"
    CONFIRMED = "Confirmed"
    EXPIRED = "Expired"
    ATTENDED = "Attended"
    REJECTED = "Rejected"
    WAITLISTED = "Waitlisted"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples containing the enum name and value.
        """
        return [(tag.name, tag.value) for tag in cls]
