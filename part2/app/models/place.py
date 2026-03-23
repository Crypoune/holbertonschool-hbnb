from app.models import BaseModel

class Place(BaseModel):
    """
    Place model representing a place to stay.
    """

    def __init__(self, name, title, description, price, latitude, longitude, owner_id):
        """
        Initialize a Place instance.
        Args:
            name (str): Short identifier for the place (e.g., "Cozy Cottage")
            title (str): Full marketing title (e.g., "Cozy Cottage in the Woods")
            description (str): Detailed description
            price (float): Price per night
            latitude (float): GPS latitude (-90 to 90)
            longitude (float): GPS longitude (-180 to 180)
            owner_id (str): UUID of the owner
        """
        super().__init__()
        self.name = name
        self.title = title
        self.description = description
        self.price = price
        self._latitude = latitude
        self._longitude = longitude
        self.owner_id = owner_id
        self.amenities = []  # List of amenity IDs (UUID strings)

    # ----------------- Latitude -----------------
    @property
    def latitude(self):
        """Getter for latitude"""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be a number between -90 and 90")
        self._latitude = value

    # ----------------- Longitude -----------------
    @property
    def longitude(self):
        """Getter for longitude"""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be a number between -180 and 180")
        self._longitude = value

    # ----------------- Amenities -----------------
    def add_amenity(self, amenity):
        """Add an amenity to the place (objet ou UUID string)."""
        amenity_id = amenity.id if hasattr(amenity, "id") else amenity
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    # ----------------- Serialization -----------------
    def to_dict(self):
        """Convert Place to dictionary."""
        place_dict = super().to_dict()
        place_dict['name'] = self.name
        place_dict['title'] = self.title
        place_dict['description'] = self.description
        place_dict['price'] = self.price
        place_dict['latitude'] = self.latitude
        place_dict['longitude'] = self.longitude
        place_dict['owner_id'] = self.owner_id
        place_dict['amenities'] = self.amenities
        return place_dict
