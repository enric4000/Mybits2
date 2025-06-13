from enum import Enum

class EnglishLevelEnum(Enum):
    """
    Enum representing the levels of English proficiency.
    """
    LOW = "Low"
    MEDIUM = "Medium"
    ADVANCED = "Advanced"
    NATIVE = "Native"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples containing the enum name and value.
        """
        return [(tag.name, tag.value) for tag in cls]
