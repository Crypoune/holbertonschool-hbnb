from app.models.base_model import BaseModel
from app import db


class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        super().__init__()
        if not name or not name.strip():
            raise ValueError("Name is required and cannot be empty")
        self.name = name

    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict['name'] = self.name
        return amenity_dict
