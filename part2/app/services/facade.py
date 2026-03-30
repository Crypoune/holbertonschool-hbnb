from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # ── User ──────────────────────────────────────────────────────────────────

    def create_user(self, user_data: dict):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id: str, data: dict):
        self.user_repo.update(user_id, data)
        return self.get_user(user_id)

    # ── Amenity ───────────────────────────────────────────────────────────────

    def create_amenity(self, amenity_data: dict):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: dict):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    # ── Place ─────────────────────────────────────────────────────────────────

    def create_place(self, place_data: dict):
        owner_id = place_data.get('owner_id')
        if not self.user_repo.get(owner_id):
            raise ValueError("Owner not found")
        place = Place(**{k: v for k, v in place_data.items()})
        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id: str, place_data: dict):
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    # ── Review ────────────────────────────────────────────────────────────────

    def create_review(self, review_data: dict):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id: str):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id: str):
        return [r for r in self.review_repo.get_all() if r.place_id == place_id]

    def update_review(self, review_id: str, data: dict):
        self.review_repo.update(review_id, data)
        return self.get_review(review_id)

    def delete_review(self, review_id: str):
        self.review_repo.delete(review_id)
