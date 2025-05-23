from enum import Enum

class DietaryEnum(Enum):
    NONE = "None"
    GLUTEN_FREE = "Gluten Free"
    VEGETARIAN = "Vegetarian"
    VEGAN = "Vegan"
    HALAL = "Halal"
    OTHER = "Other"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples containing the enum name and value.
        """
        return [(tag.name, tag.value) for tag in cls]
