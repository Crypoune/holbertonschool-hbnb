from app.models import BaseModel

class Amenity(BaseModel):
    """
        Amenity model representing an amenity that can be associated with a place.
        E.g., "WiFi", "Pool", "Air Conditioning", Parking", etc.
    """

    def __init__(self, name, description=""):
        """
            Initialize an Amenity instance
            Args:
                name (str): Name of the amenity (e.g., "WiFi", "Pool")
                description (str): Optional description of the amenity
        """
        super().__init__() # Call __init__ of BaseModel
        if not name or not name.strip():
            raise ValueError("Name is required and cannot be empty")
        self.name = name
        self.description = description

    def to_dict(self):
        """Convert Amenity to dictionary"""
        amenity_dict = super().to_dict()
        amenity_dict['name'] = self.name
        amenity_dict['description'] = self.description
        return amenity_dict
