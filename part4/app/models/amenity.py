from app.models.base_model import BaseModel
from app import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    def __init__(self, name, image_url=None):
        super().__init__()
        if not name or not name.strip():
            raise ValueError("Name is required and cannot be empty")
        self.name = name
        self.image_url = image_url
        self.name = name

    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict['name'] = self.name
        amenity_dict['image_url'] = self.image_url
        return amenity_dict
