from app.models.base_model import BaseModel
from app import db

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), default='')
    _price = db.Column('price', db.Float, nullable=False)
    _latitude = db.Column('latitude', db.Float, nullable=False)
    _longitude = db.Column('longitude', db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    owner = db.relationship('User', backref='places', lazy=True)
    reviews = db.relationship('Review', backref='place', cascade='all, delete-orphan')
    amenities = db.relationship(
    'Amenity',
    secondary=place_amenity,
    backref=db.backref('places', lazy=True),
    lazy='subquery'
)

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.amenities = []

 # ----------------- Price -----------------

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = value

    # ----------------- Latitude -----------------

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not (-90 <= value <= 90):
            raise ValueError("Latitude must be a number between -90 and 90")
        self._latitude = value

    # ----------------- Longitude -----------------

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not (-180 <= value <= 180):
            raise ValueError("Longitude must be a number between -180 and 180")
        self._longitude = value

    # ----------------- Serialization -----------------

    def to_dict(self):
        place_dict = super().to_dict()
        place_dict['title'] = self.title
        place_dict['description'] = self.description
        place_dict['price'] = self.price
        place_dict['latitude'] = self.latitude
        place_dict['longitude'] = self.longitude
        place_dict['owner_id'] = self.owner_id
        place_dict['amenities'] = [a.to_dict() for a in self.amenities]
        return place_dict
