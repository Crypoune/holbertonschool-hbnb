from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.services.repositories.amenity_repository import AmenityRepository
from app.services.repositories.place_repository import PlaceRepository
from app.services.repositories.review_repository import ReviewRepository
from app.services.repositories.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        self.user_repo     = UserRepository()
        self.place_repo    = PlaceRepository()
        self.amenity_repo  = AmenityRepository()
        self.review_repo   = ReviewRepository()

    # ── User ──────────────────────────────────────────────────────────────────

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id: str, data: dict):
        data = dict(data)
        obj = self.user_repo.get(user_id)
        if obj and 'password' in data:
            obj.password = data.pop('password')  # passe par le setter qui hashe
        if data:
            self.user_repo.update(user_id, data)
        return self.get_user(user_id)

    # ── Amenity ───────────────────────────────────────────────────────────────

    def create_amenity(self, amenity_data):
        amenity = Amenity(name=amenity_data['name'])
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.get_amenity(amenity_id)

    # ── Place ─────────────────────────────────────────────────────────────────

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        if not self.user_repo.get(owner_id):
            raise ValueError("Owner not found")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=owner_id
        )

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
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
        # 👇 Retire le "self," en premier argument !
        return self.review_repo.get_reviews_by_place(place_id)

    def update_review(self, review_id: str, data: dict):
        self.review_repo.update(review_id, data)

    def delete_review(self, review_id: str):
        self.review_repo.delete(review_id)
