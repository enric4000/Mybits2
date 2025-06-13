from enum import Enum


class ActivityEnum(Enum):
    NORMALACTIVITY = "Normal Activity"
    WORKSHOP = "Workshop"
    MEAL = "Meal"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples containing the enum name and value.
        """
        return [(tag.name, tag.value) for tag in cls]
