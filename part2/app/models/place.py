from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = []

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value

    def add_amenity(self, amenity):
        amenity_id = amenity.id if hasattr(amenity, "id") else amenity
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def to_dict(self):
        d = super().to_dict()
        d['title'] = self.title
        d['description'] = self.description
        d['price'] = self.price
        d['latitude'] = self.latitude
        d['longitude'] = self.longitude
        d['owner_id'] = self.owner_id
        d['amenities'] = self.amenities
        return d
