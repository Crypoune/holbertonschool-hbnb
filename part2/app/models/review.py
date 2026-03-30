from app.models.base_model import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        if not text or not text.strip():
            raise ValueError("Text is required and cannot be empty")
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not (1 <= value <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")
        self._rating = value

    def to_dict(self):
        d = super().to_dict()
        d['text'] = self.text
        d['rating'] = self.rating
        d['user_id'] = self.user_id
        d['place_id'] = self.place_id
        return d
