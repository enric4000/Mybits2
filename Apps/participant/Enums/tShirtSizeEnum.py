from enum import Enum

class TShirtSizeEnum(Enum):
    """
    Enum representing the sizes of t-shirts.
    """
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    XXXL = "XXXL"

    @classmethod
    def choices(cls):
        """
        Returns a list of tuples containing the enum name and value.
        """
        return [(tag.name, tag.value) for tag in cls]
