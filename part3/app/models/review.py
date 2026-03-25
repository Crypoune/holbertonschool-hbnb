from app.models.base_model import BaseModel
from app import db


class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1000), nullable=False)
    _rating = db.Column('rating', db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    # Relationships
    place = db.relationship('Place', backref='reviews', lazy=True)
    user = db.relationship('User', backref='reviews', lazy=True)

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
        review_dict = super().to_dict()
        review_dict['text'] = self.text
        review_dict['rating'] = self.rating
        review_dict['user_id'] = self.user_id
        review_dict['place_id'] = self.place_id
        return review_dict
