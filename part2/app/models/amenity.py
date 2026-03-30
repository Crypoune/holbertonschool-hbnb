from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()
        if not name or not name.strip():
            raise ValueError("Name is required and cannot be empty")
        self.name = name
        self.description = description

    def to_dict(self):
        d = super().to_dict()
        d['name'] = self.name
        d['description'] = self.description
        return d
