from enum import Enum


class GenderEnum(Enum):
    MALE = "Male"
    FEMALE = "Female"
    NOT_SPECIFIED = "Not Specified"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples containing the enum name and value.
        """
        return [(tag.name, tag.value) for tag in cls]
