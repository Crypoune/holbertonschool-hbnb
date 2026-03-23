"""
test_hbnb_api.py
================
Tests complets pour tous les endpoints de l'API HBnB - Partie 2.
Couvre : Users, Amenities, Places, Reviews

Lancement :
    python -m pytest tests/test_hbnb_api.py -v
"""

import pytest
from app import create_app


# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    """Fresh test client for every test."""
    # Reset le facade directement
    import app.services as services_module
    from app.services.facade import HBnBFacade
    services_module.facade = HBnBFacade()

    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def create_user(client, first_name="Arnaud", last_name="Messenet",
                email="arnaud.messenet@example.com", password="securepass"):
    return client.post('/api/v1/users/', json={
        "first_name": first_name,
        "last_name":  last_name,
        "email":      email,
        "password":   password,
    })

def create_amenity(client, name="WiFi"):
    return client.post('/api/v1/amenities/', json={"name": name})

def create_place(client, owner_id, title="Cozy Flat",
                 price=80.0, latitude=48.8, longitude=2.3):
    return client.post('/api/v1/places/', json={
        "title":       title,
        "description": "A nice place",
        "price":       price,
        "latitude":    latitude,
        "longitude":   longitude,
        "owner_id":    owner_id,
    })

def create_review(client, place_id, user_id, text="Great!", rating=5):
    return client.post('/api/v1/reviews/', json={
        "text":     text,
        "rating":   rating,
        "place_id": place_id,
        "user_id":  user_id,
    })


# ═════════════════════════════════════════════════════════════════════════════
# 1. USERS
# ═════════════════════════════════════════════════════════════════════════════

class TestUsers:

    # ── POST /api/v1/users/ ───────────────────────────────────────────────────

    def test_create_user_success(self, client):
        resp = create_user(client)
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'id' in data
        assert data['first_name'] == 'Arnaud'
        assert data['email'] == 'arnaud.messenet@example.com'

    def test_create_user_missing_fields(self, client):
        resp = client.post('/api/v1/users/', json={})
        assert resp.status_code in [400, 422]

    def test_create_user_empty_first_name(self, client):
        resp = create_user(client, first_name="")
        assert resp.status_code in [400, 422]

    def test_create_user_invalid_email(self, client):
        resp = create_user(client, email="not-an-email")
        assert resp.status_code in [400, 422]

    def test_create_user_duplicate_email(self, client):
        create_user(client, email="valentin.dardenne@example.com")
        resp = create_user(client, email="valentin.dardenne@example.com")
        assert resp.status_code in [400, 409]

    # ── GET /api/v1/users/ ────────────────────────────────────────────────────

    def test_list_users(self, client):
        create_user(client, email="thomas.haenel@example.com")
        resp = client.get('/api/v1/users/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_list_users_empty(self, client):
        resp = client.get('/api/v1/users/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    # ── GET /api/v1/users/<id> ────────────────────────────────────────────────

    def test_get_user_by_id(self, client):
        user_id = create_user(client, email="valentin.dardenne@example.com").get_json()['id']
        resp = client.get(f'/api/v1/users/{user_id}')
        assert resp.status_code == 200
        assert resp.get_json()['id'] == user_id

    def test_get_user_not_found(self, client):
        resp = client.get('/api/v1/users/nonexistent-id')
        assert resp.status_code == 404

    # ── PUT /api/v1/users/<id> ────────────────────────────────────────────────

    def test_update_user(self, client):
        user_id = create_user(client, email="arnaud.messenet@example.com").get_json()['id']
        resp = client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Thomas",
            "last_name":  "Haenel",
            "email":      "thomas.haenel@example.com",
            "password":   "newpassword",
        })
        assert resp.status_code == 200
        assert resp.get_json()['first_name'] == 'Thomas'

    def test_update_user_not_found(self, client):
        resp = client.put('/api/v1/users/nonexistent-id', json={
            "first_name": "X", "last_name": "Y",
            "email": "x@y.com", "password": "pass1234",
        })
        assert resp.status_code == 404


# ═════════════════════════════════════════════════════════════════════════════
# 2. AMENITIES
# ═════════════════════════════════════════════════════════════════════════════

class TestAmenities:

    # ── POST /api/v1/amenities/ ───────────────────────────────────────────────

    def test_create_amenity_success(self, client):
        resp = create_amenity(client, "Pool")
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'id' in data
        assert data['name'] == 'Pool'

    def test_create_amenity_missing_name(self, client):
        resp = client.post('/api/v1/amenities/', json={})
        assert resp.status_code in [400, 422]

    def test_create_amenity_empty_name(self, client):
        resp = client.post('/api/v1/amenities/', json={"name": ""})
        assert resp.status_code in [400, 422]

    # ── GET /api/v1/amenities/ ────────────────────────────────────────────────

    def test_list_amenities(self, client):
        create_amenity(client, "WiFi")
        resp = client.get('/api/v1/amenities/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    def test_list_amenities_empty(self, client):
        resp = client.get('/api/v1/amenities/')
        assert resp.status_code == 200
        assert resp.get_json() == []

    # ── GET /api/v1/amenities/<id> ────────────────────────────────────────────

    def test_get_amenity_by_id(self, client):
        amenity_id = create_amenity(client, "Parking").get_json()['id']
        resp = client.get(f'/api/v1/amenities/{amenity_id}')
        assert resp.status_code == 200
        assert resp.get_json()['name'] == 'Parking'

    def test_get_amenity_not_found(self, client):
        resp = client.get('/api/v1/amenities/nonexistent-id')
        assert resp.status_code == 404

    # ── PUT /api/v1/amenities/<id> ────────────────────────────────────────────

    def test_update_amenity(self, client):
        amenity_id = create_amenity(client, "Jacuzzi").get_json()['id']
        resp = client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Hot Tub"})
        assert resp.status_code == 200
        assert resp.get_json()['name'] == 'Hot Tub'

    def test_update_amenity_not_found(self, client):
        resp = client.put('/api/v1/amenities/nonexistent-id', json={"name": "X"})
        assert resp.status_code == 404


# ═════════════════════════════════════════════════════════════════════════════
# 3. PLACES
# ═════════════════════════════════════════════════════════════════════════════

class TestPlaces:

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.owner_id = create_user(client, email="arnaud.messenet@example.com").get_json()['id']

    # ── POST /api/v1/places/ ─────────────────────────────────────────────────

    def test_create_place_success(self, client):
        resp = create_place(client, self.owner_id)
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'id' in data
        assert data['owner_id'] == self.owner_id

    def test_create_place_invalid_owner(self, client):
        resp = create_place(client, "nonexistent-owner-id")
        assert resp.status_code in [400, 404]

    def test_create_place_negative_price(self, client):
        resp = create_place(client, self.owner_id, price=-10.0)
        assert resp.status_code in [400, 422]

    def test_create_place_zero_price(self, client):
        resp = create_place(client, self.owner_id, price=0)
        assert resp.status_code in [400, 422]

    def test_create_place_invalid_latitude(self, client):
        resp = create_place(client, self.owner_id, latitude=100.0)
        assert resp.status_code in [400, 422]

    def test_create_place_invalid_longitude(self, client):
        resp = create_place(client, self.owner_id, longitude=200.0)
        assert resp.status_code in [400, 422]

    def test_create_place_missing_title(self, client):
        resp = client.post('/api/v1/places/', json={
            "price": 50.0, "latitude": 48.0,
            "longitude": 2.0, "owner_id": self.owner_id,
        })
        assert resp.status_code in [400, 422]

    # ── GET /api/v1/places/ ───────────────────────────────────────────────────

    def test_list_places(self, client):
        create_place(client, self.owner_id)
        resp = client.get('/api/v1/places/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    # ── GET /api/v1/places/<id> ───────────────────────────────────────────────

    def test_get_place_by_id(self, client):
        place_id = create_place(client, self.owner_id).get_json()['id']
        resp = client.get(f'/api/v1/places/{place_id}')
        assert resp.status_code == 200
        assert 'owner' in resp.get_json()

    def test_get_place_not_found(self, client):
        resp = client.get('/api/v1/places/nonexistent-id')
        assert resp.status_code == 404

    # ── PUT /api/v1/places/<id> ───────────────────────────────────────────────

    def test_update_place(self, client):
        place_id = create_place(client, self.owner_id).get_json()['id']
        resp = client.put(f'/api/v1/places/{place_id}', json={
            "title":       "Updated Title",
            "description": "Updated desc",
            "price":       120.0,
            "latitude":    45.0,
            "longitude":   9.0,
            "owner_id":    self.owner_id,
        })
        assert resp.status_code == 200
        assert resp.get_json()['title'] == 'Updated Title'

    def test_update_place_not_found(self, client):
        resp = client.put('/api/v1/places/nonexistent-id', json={
            "title": "X", "price": 10.0,
            "latitude": 0.0, "longitude": 0.0,
            "owner_id": self.owner_id,
        })
        assert resp.status_code == 404

    # ── Boundary tests ────────────────────────────────────────────────────────

    def test_create_place_boundary_latitude_min(self, client):
        resp = create_place(client, self.owner_id, latitude=-90.0)
        assert resp.status_code == 201

    def test_create_place_boundary_latitude_max(self, client):
        resp = create_place(client, self.owner_id, latitude=90.0)
        assert resp.status_code == 201

    def test_create_place_boundary_longitude_min(self, client):
        resp = create_place(client, self.owner_id, longitude=-180.0)
        assert resp.status_code == 201

    def test_create_place_boundary_longitude_max(self, client):
        resp = create_place(client, self.owner_id, longitude=180.0)
        assert resp.status_code == 201

    # ── GET /api/v1/places/<id>/reviews ──────────────────────────────────────

    def test_get_reviews_by_place_empty(self, client):
        place_id = create_place(client, self.owner_id).get_json()['id']
        resp = client.get(f'/api/v1/places/{place_id}/reviews')
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_get_reviews_by_invalid_place(self, client):
        resp = client.get('/api/v1/places/nonexistent-id/reviews')
        assert resp.status_code == 404


# ═════════════════════════════════════════════════════════════════════════════
# 4. REVIEWS
# ═════════════════════════════════════════════════════════════════════════════

class TestReviews:

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.client = client
        self.user_id  = create_user(client, email="valentin.dardenne@example.com").get_json()['id']
        self.owner_id = create_user(client, email="thomas.haenel@example.com").get_json()['id']
        self.place_id = create_place(client, self.owner_id).get_json()['id']

    # ── POST /api/v1/reviews/ ─────────────────────────────────────────────────

    def test_create_review_success(self, client):
        resp = create_review(client, self.place_id, self.user_id)
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'id' in data
        assert data['rating'] == 5

    def test_create_review_invalid_place(self, client):
        resp = create_review(client, "bad-place-id", self.user_id)
        assert resp.status_code in [400, 404]

    def test_create_review_invalid_user(self, client):
        resp = create_review(client, self.place_id, "bad-user-id")
        assert resp.status_code in [400, 404]

    def test_create_review_empty_text(self, client):
        resp = client.post('/api/v1/reviews/', json={
            "text": "", "rating": 3,
            "place_id": self.place_id, "user_id": self.user_id,
        })
        assert resp.status_code in [400, 422]

    def test_create_review_rating_too_high(self, client):
        resp = client.post('/api/v1/reviews/', json={
            "text": "OK", "rating": 6,
            "place_id": self.place_id, "user_id": self.user_id,
        })
        assert resp.status_code in [400, 422]

    def test_create_review_rating_too_low(self, client):
        resp = client.post('/api/v1/reviews/', json={
            "text": "OK", "rating": 0,
            "place_id": self.place_id, "user_id": self.user_id,
        })
        assert resp.status_code in [400, 422]

    def test_create_review_missing_rating(self, client):
        resp = client.post('/api/v1/reviews/', json={
            "text": "OK",
            "place_id": self.place_id, "user_id": self.user_id,
        })
        assert resp.status_code in [400, 422]

    # ── GET /api/v1/reviews/ ──────────────────────────────────────────────────

    def test_list_reviews(self, client):
        create_review(client, self.place_id, self.user_id)
        resp = client.get('/api/v1/reviews/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)

    # ── GET /api/v1/reviews/<id> ──────────────────────────────────────────────

    def test_get_review_by_id(self, client):
        review_id = create_review(client, self.place_id, self.user_id).get_json()['id']
        resp = client.get(f'/api/v1/reviews/{review_id}')
        assert resp.status_code == 200
        assert resp.get_json()['id'] == review_id

    def test_get_review_not_found(self, client):
        resp = client.get('/api/v1/reviews/nonexistent-id')
        assert resp.status_code == 404

    # ── PUT /api/v1/reviews/<id> ──────────────────────────────────────────────

    def test_update_review(self, client):
        review_id = create_review(client, self.place_id, self.user_id).get_json()['id']
        resp = client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated text", "rating": 4,
            "place_id": self.place_id, "user_id": self.user_id,
        })
        assert resp.status_code == 200
        assert resp.get_json()['text'] == 'Updated text'

    def test_update_review_not_found(self, client):
        resp = client.put('/api/v1/reviews/nonexistent-id', json={
            "text": "X", "rating": 3,
            "place_id": self.place_id, "user_id": self.user_id,
        })
        assert resp.status_code == 404

    # ── DELETE /api/v1/reviews/<id> ───────────────────────────────────────────

    def test_delete_review(self, client):
        review_id = create_review(client, self.place_id, self.user_id).get_json()['id']
        resp = client.delete(f'/api/v1/reviews/{review_id}')
        assert resp.status_code == 200
        assert client.get(f'/api/v1/reviews/{review_id}').status_code == 404

    def test_delete_review_not_found(self, client):
        resp = client.delete('/api/v1/reviews/nonexistent-id')
        assert resp.status_code == 404

    # ── GET /api/v1/places/<place_id>/reviews ────────────────────────────────

    def test_get_reviews_by_place(self, client):
        create_review(client, self.place_id, self.user_id, text="Nice", rating=4)
        resp = client.get(f'/api/v1/places/{self.place_id}/reviews')
        assert resp.status_code == 200
        reviews = resp.get_json()
        assert all(r['place_id'] == self.place_id for r in reviews)

    def test_get_reviews_by_invalid_place(self, client):
        resp = client.get('/api/v1/places/nonexistent-id/reviews')
        assert resp.status_code == 404
