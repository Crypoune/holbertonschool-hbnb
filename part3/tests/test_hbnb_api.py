"""
test_hbnb_api.py
================
Tests complets pour tous les endpoints de l'API HBnB - Partie 3.
Couvre : Authentification JWT, Users, Amenities, Places, Reviews
         avec contrôle d'accès (admin vs user normal) et base SQLite en mémoire.
 
Lancement :
    python -m pytest tests/test_hbnb_api.py -v
"""
 
import pytest
from app import create_app, db
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Configuration de test
# ─────────────────────────────────────────────────────────────────────────────
 
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'test-secret-key'
    SECRET_KEY = 'test-secret-key'
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────
 
@pytest.fixture(scope='function')
def app():
    """Crée une instance de l'app avec SQLite en mémoire pour chaque test."""
    application = create_app()
    application.config.from_object(TestConfig)
 
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()
 
 
@pytest.fixture
def client(app):
    """Client de test Flask."""
    return app.test_client()
 
 
@pytest.fixture
def admin_token(client):
    """Crée un admin et retourne son token JWT."""
    # On enregistre l'admin directement en base pour éviter la dépendance circulaire
    from app.models.user import User
    from app import db as _db
    admin = User(
        first_name="Admin",
        last_name="User",
        email="admin@hbnb.com",
        password="adminpass123",
        is_admin=True
    )
    _db.session.add(admin)
    _db.session.commit()
 
    resp = client.post('/api/v1/auth/login', json={
        "email": "admin@hbnb.com",
        "password": "adminpass123"
    })
    assert resp.status_code == 200, f"Admin login failed: {resp.get_json()}"
    return resp.get_json()['access_token']
 
 
@pytest.fixture
def user_token(client, admin_token):
    """Crée un user normal et retourne son token JWT."""
    resp = _create_user(client, admin_token,
                        first_name="Regular",
                        last_name="User",
                        email="regular@hbnb.com",
                        password="userpass123")
    assert resp.status_code == 201, f"User creation failed: {resp.get_json()}"
    user_id = resp.get_json()['id']
 
    resp = client.post('/api/v1/auth/login', json={
        "email": "regular@hbnb.com",
        "password": "userpass123"
    })
    assert resp.status_code == 200
    token = resp.get_json()['access_token']
    return token, user_id
 
 
# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
 
def auth_headers(token):
    """Retourne les headers d'authentification JWT."""
    return {'Authorization': f'Bearer {token}'}
 
 
def _create_user(client, token, first_name="Arnaud", last_name="Messenet",
                 email="arnaud.messenet@example.com", password="password123"):
    return client.post('/api/v1/users/', json={
        "first_name": first_name,
        "last_name":  last_name,
        "email":      email,
        "password":   password,
    }, headers=auth_headers(token))
 
 
def _create_amenity(client, token, name="WiFi"):
    return client.post('/api/v1/amenities/', json={"name": name},
                       headers=auth_headers(token))
 
 
def _create_place(client, token, owner_id, title="Cozy Flat",
                  price=80.0, latitude=48.8, longitude=2.3):
    return client.post('/api/v1/places/', json={
        "title":       title,
        "description": "A nice place",
        "price":       price,
        "latitude":    latitude,
        "longitude":   longitude,
        "owner_id":    owner_id,
    }, headers=auth_headers(token))
 
 
def _create_review(client, token, place_id, user_id, text="Great!", rating=5):
    return client.post('/api/v1/reviews/', json={
        "text":     text,
        "rating":   rating,
        "place_id": place_id,
        "user_id":  user_id,
    }, headers=auth_headers(token))
 
 
# ═════════════════════════════════════════════════════════════════════════════
# 1. AUTHENTIFICATION JWT
# ═════════════════════════════════════════════════════════════════════════════
 
class TestAuth:
 
    def test_login_success(self, client, admin_token):
        """Login avec des credentials valides retourne un token."""
        resp = client.post('/api/v1/auth/login', json={
            "email": "admin@hbnb.com",
            "password": "adminpass123"
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'access_token' in data
 
    def test_login_wrong_password(self, client, admin_token):
        """Login avec un mauvais mot de passe retourne 401."""
        resp = client.post('/api/v1/auth/login', json={
            "email": "admin@hbnb.com",
            "password": "wrongpassword"
        })
        assert resp.status_code == 401
 
    def test_login_unknown_email(self, client):
        """Login avec un email inconnu retourne 401."""
        resp = client.post('/api/v1/auth/login', json={
            "email": "nobody@hbnb.com",
            "password": "somepassword"
        })
        assert resp.status_code == 401
 
    def test_login_missing_fields(self, client):
        """Login sans champs requis retourne 400."""
        resp = client.post('/api/v1/auth/login', json={})
        assert resp.status_code in [400, 401]
 
    def test_protected_endpoint_with_valid_token(self, client, admin_token):
        """Endpoint protégé accessible avec un token valide."""
        resp = client.get('/api/v1/auth/protected',
                          headers=auth_headers(admin_token))
        assert resp.status_code == 200
 
    def test_protected_endpoint_without_token(self, client):
        """Endpoint protégé inaccessible sans token."""
        resp = client.get('/api/v1/auth/protected')
        assert resp.status_code == 401
 
    def test_protected_endpoint_with_invalid_token(self, client):
        """Endpoint protégé inaccessible avec un token invalide."""
        resp = client.get('/api/v1/auth/protected',
                          headers=auth_headers("token.invalide.ici"))
        assert resp.status_code == 422
 
 
# ═════════════════════════════════════════════════════════════════════════════
# 2. USERS
# ═════════════════════════════════════════════════════════════════════════════
 
class TestUsers:
 
    def test_create_user_as_admin(self, client, admin_token):
        """Un admin peut créer un utilisateur."""
        resp = _create_user(client, admin_token)
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'id' in data
        assert data['first_name'] == 'Arnaud'
        assert data['email'] == 'arnaud.messenet@example.com'
        assert 'password' not in data  # Le mot de passe ne doit pas être exposé
 
    def test_create_user_as_regular_user(self, client, user_token):
        """Un user normal ne peut pas créer un utilisateur."""
        token, _ = user_token
        resp = _create_user(client, token, email="new@hbnb.com")
        assert resp.status_code == 403
 
    def test_create_user_without_token(self, client):
        """Créer un user sans token retourne 401."""
        resp = client.post('/api/v1/users/', json={
            "first_name": "X", "last_name": "Y",
            "email": "x@y.com", "password": "pass1234"
        })
        assert resp.status_code == 401
 
    def test_create_user_missing_fields(self, client, admin_token):
        """Créer un user sans champs requis retourne 400."""
        resp = client.post('/api/v1/users/', json={},
                           headers=auth_headers(admin_token))
        assert resp.status_code in [400, 422]
 
    def test_create_user_empty_first_name(self, client, admin_token):
        """Prénom vide retourne 400."""
        resp = _create_user(client, admin_token, first_name="")
        assert resp.status_code in [400, 422]
 
    def test_create_user_invalid_email(self, client, admin_token):
        """Email invalide retourne 400."""
        resp = _create_user(client, admin_token, email="not-an-email")
        assert resp.status_code in [400, 422]
 
    def test_create_user_duplicate_email(self, client, admin_token):
        """Email déjà utilisé retourne 400."""
        _create_user(client, admin_token, email="valentin.dardenne@example.com")
        resp = _create_user(client, admin_token, email="valentin.dardenne@example.com")
        assert resp.status_code in [400, 409]
 
    def test_create_user_password_too_short(self, client, admin_token):
        """Mot de passe trop court retourne 400."""
        resp = _create_user(client, admin_token, password="abc")
        assert resp.status_code in [400, 422]
 
    def test_list_users_public(self, client, admin_token):
        """Lister les users est accessible sans token."""
        _create_user(client, admin_token, email="thomas.haenel@example.com")
        resp = client.get('/api/v1/users/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)
 
    def test_list_users_empty(self, client):
        """Liste vide si aucun user."""
        resp = client.get('/api/v1/users/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)
 
    def test_get_user_by_id(self, client, admin_token):
        """Récupérer un user par son ID."""
        user_id = _create_user(client, admin_token,
                                email="valentin.dardenne@example.com").get_json()['id']
        resp = client.get(f'/api/v1/users/{user_id}')
        assert resp.status_code == 200
        assert resp.get_json()['id'] == user_id
 
    def test_get_user_not_found(self, client):
        """User inexistant retourne 404."""
        resp = client.get('/api/v1/users/nonexistent-id')
        assert resp.status_code == 404
 
    def test_update_own_profile(self, client, user_token):
        """Un user peut modifier son propre prénom/nom."""
        token, user_id = user_token
        resp = client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Updated",
            "last_name":  "Name",
        }, headers=auth_headers(token))
        assert resp.status_code == 200
        assert resp.get_json()['first_name'] == 'Updated'
 
    def test_update_own_email_forbidden(self, client, user_token):
        """Un user normal ne peut pas modifier son email."""
        token, user_id = user_token
        resp = client.put(f'/api/v1/users/{user_id}', json={
            "email": "newemail@hbnb.com",
        }, headers=auth_headers(token))
        assert resp.status_code == 400
 
    def test_update_own_password_forbidden(self, client, user_token):
        """Un user normal ne peut pas modifier son mot de passe."""
        token, user_id = user_token
        resp = client.put(f'/api/v1/users/{user_id}', json={
            "password": "newpassword123",
        }, headers=auth_headers(token))
        assert resp.status_code == 400
 
    def test_update_other_user_forbidden(self, client, user_token, admin_token):
        """Un user normal ne peut pas modifier un autre user."""
        token, _ = user_token
        other_id = _create_user(client, admin_token,
                                 email="other@hbnb.com").get_json()['id']
        resp = client.put(f'/api/v1/users/{other_id}', json={
            "first_name": "Hacked",
            "last_name": "User",
        }, headers=auth_headers(token))
        assert resp.status_code == 403
 
    def test_admin_can_update_any_user(self, client, admin_token, user_token):
        """Un admin peut modifier n'importe quel user."""
        _, user_id = user_token
        resp = client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "AdminUpdated",
            "last_name":  "ByAdmin",
            "email":      "adminupdated@hbnb.com",
        }, headers=auth_headers(admin_token))
        assert resp.status_code == 200
        assert resp.get_json()['first_name'] == 'AdminUpdated'
 
    def test_update_user_not_found(self, client, admin_token):
        """Mettre à jour un user inexistant retourne 404."""
        resp = client.put('/api/v1/users/nonexistent-id', json={
            "first_name": "X", "last_name": "Y",
        }, headers=auth_headers(admin_token))
        assert resp.status_code == 404
 
    def test_update_user_without_token(self, client, admin_token):
        """Mettre à jour un user sans token retourne 401."""
        user_id = _create_user(client, admin_token,
                                email="target@hbnb.com").get_json()['id']
        resp = client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "X", "last_name": "Y",
        })
        assert resp.status_code == 401
 
 
# ═════════════════════════════════════════════════════════════════════════════
# 3. AMENITIES
# ═════════════════════════════════════════════════════════════════════════════
 
class TestAmenities:
 
    def test_create_amenity_as_admin(self, client, admin_token):
        """Un admin peut créer une amenity."""
        resp = _create_amenity(client, admin_token, "Pool")
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'id' in data
        assert data['name'] == 'Pool'
 
    def test_create_amenity_as_regular_user(self, client, user_token):
        """Un user normal ne peut pas créer une amenity (selon votre impl)."""
        token, _ = user_token
        resp = _create_amenity(client, token, "Pool")
        # Adaptez selon votre logique : 403 si admin requis, 201 si ouvert à tous
        assert resp.status_code in [201, 403]
 
    def test_create_amenity_without_token(self, client):
        """Créer une amenity sans token retourne 401."""
        resp = client.post('/api/v1/amenities/', json={"name": "WiFi"})
        assert resp.status_code in [401, 403]
 
    def test_create_amenity_missing_name(self, client, admin_token):
        """Amenity sans nom retourne 400."""
        resp = client.post('/api/v1/amenities/', json={},
                           headers=auth_headers(admin_token))
        assert resp.status_code in [400, 422]
 
    def test_create_amenity_empty_name(self, client, admin_token):
        """Amenity avec nom vide retourne 400."""
        resp = client.post('/api/v1/amenities/', json={"name": ""},
                           headers=auth_headers(admin_token))
        assert resp.status_code in [400, 422]
 
    def test_list_amenities(self, client, admin_token):
        """Lister les amenities est public."""
        _create_amenity(client, admin_token, "WiFi")
        resp = client.get('/api/v1/amenities/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)
 
    def test_list_amenities_empty(self, client):
        """Liste vide si aucune amenity."""
        resp = client.get('/api/v1/amenities/')
        assert resp.status_code == 200
        assert resp.get_json() == []
 
    def test_get_amenity_by_id(self, client, admin_token):
        """Récupérer une amenity par son ID."""
        amenity_id = _create_amenity(client, admin_token, "Parking").get_json()['id']
        resp = client.get(f'/api/v1/amenities/{amenity_id}')
        assert resp.status_code == 200
        assert resp.get_json()['name'] == 'Parking'
 
    def test_get_amenity_not_found(self, client):
        """Amenity inexistante retourne 404."""
        resp = client.get('/api/v1/amenities/nonexistent-id')
        assert resp.status_code == 404
 
    def test_update_amenity_as_admin(self, client, admin_token):
        """Un admin peut modifier une amenity."""
        amenity_id = _create_amenity(client, admin_token, "Jacuzzi").get_json()['id']
        resp = client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Hot Tub"},
                          headers=auth_headers(admin_token))
        assert resp.status_code == 200
        assert resp.get_json()['name'] == 'Hot Tub'
 
    def test_update_amenity_not_found(self, client, admin_token):
        """Modifier une amenity inexistante retourne 404."""
        resp = client.put('/api/v1/amenities/nonexistent-id', json={"name": "X"},
                          headers=auth_headers(admin_token))
        assert resp.status_code == 404
 
 
# ═════════════════════════════════════════════════════════════════════════════
# 4. PLACES
# ═════════════════════════════════════════════════════════════════════════════
 
class TestPlaces:
 
    @pytest.fixture(autouse=True)
    def setup(self, client, admin_token, user_token):
        self.client = client
        self.admin_token = admin_token
        self.user_token, self.user_id = user_token
        # Le user normal est propriétaire du logement
        self.owner_id = self.user_id
 
    def test_create_place_authenticated(self, client):
        """Un user connecté peut créer un logement."""
        resp = _create_place(client, self.user_token, self.owner_id)
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'id' in data
        assert data['owner_id'] == self.owner_id
 
    def test_create_place_without_token(self, client):
        """Créer un logement sans token retourne 401."""
        resp = client.post('/api/v1/places/', json={
            "title": "Test", "price": 50.0,
            "latitude": 48.0, "longitude": 2.0,
            "owner_id": self.owner_id,
        })
        assert resp.status_code == 401
 
    def test_create_place_invalid_owner(self, client):
        """Logement avec un owner inexistant retourne 400/404."""
        resp = _create_place(client, self.user_token, "nonexistent-owner-id")
        assert resp.status_code in [400, 404]
 
    def test_create_place_negative_price(self, client):
        """Prix négatif retourne 400."""
        resp = _create_place(client, self.user_token, self.owner_id, price=-10.0)
        assert resp.status_code in [400, 422]
 
    def test_create_place_zero_price(self, client):
        """Prix à zéro retourne 400."""
        resp = _create_place(client, self.user_token, self.owner_id, price=0)
        assert resp.status_code in [400, 422]
 
    def test_create_place_invalid_latitude(self, client):
        """Latitude invalide (> 90) retourne 400."""
        resp = _create_place(client, self.user_token, self.owner_id, latitude=100.0)
        assert resp.status_code in [400, 422]
 
    def test_create_place_invalid_longitude(self, client):
        """Longitude invalide (> 180) retourne 400."""
        resp = _create_place(client, self.user_token, self.owner_id, longitude=200.0)
        assert resp.status_code in [400, 422]
 
    def test_create_place_missing_title(self, client):
        """Logement sans titre retourne 400."""
        resp = client.post('/api/v1/places/', json={
            "price": 50.0, "latitude": 48.0,
            "longitude": 2.0, "owner_id": self.owner_id,
        }, headers=auth_headers(self.user_token))
        assert resp.status_code in [400, 422]
 
    def test_list_places_public(self, client):
        """Lister les logements est public."""
        _create_place(client, self.user_token, self.owner_id)
        resp = client.get('/api/v1/places/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)
 
    def test_get_place_by_id(self, client):
        """Récupérer un logement par son ID."""
        place_id = _create_place(client, self.user_token, self.owner_id).get_json()['id']
        resp = client.get(f'/api/v1/places/{place_id}')
        assert resp.status_code == 200
        assert 'owner' in resp.get_json()
 
    def test_get_place_not_found(self, client):
        """Logement inexistant retourne 404."""
        resp = client.get('/api/v1/places/nonexistent-id')
        assert resp.status_code == 404
 
    def test_update_place_as_owner(self, client):
        """Le propriétaire peut modifier son logement."""
        place_id = _create_place(client, self.user_token, self.owner_id).get_json()['id']
        resp = client.put(f'/api/v1/places/{place_id}', json={
            "title":       "Updated Title",
            "description": "Updated desc",
            "price":       120.0,
            "latitude":    45.0,
            "longitude":   9.0,
            "owner_id":    self.owner_id,
        }, headers=auth_headers(self.user_token))
        assert resp.status_code == 200
        assert resp.get_json()['title'] == 'Updated Title'
 
    def test_update_place_as_admin(self, client):
        """Un admin peut modifier n'importe quel logement."""
        place_id = _create_place(client, self.user_token, self.owner_id).get_json()['id']
        resp = client.put(f'/api/v1/places/{place_id}', json={
            "title":       "Admin Updated",
            "description": "By admin",
            "price":       90.0,
            "latitude":    45.0,
            "longitude":   9.0,
            "owner_id":    self.owner_id,
        }, headers=auth_headers(self.admin_token))
        assert resp.status_code == 200
 
    def test_update_place_not_found(self, client):
        """Modifier un logement inexistant retourne 404."""
        resp = client.put('/api/v1/places/nonexistent-id', json={
            "title": "X", "price": 10.0,
            "latitude": 0.0, "longitude": 0.0,
            "owner_id": self.owner_id,
        }, headers=auth_headers(self.user_token))
        assert resp.status_code == 404
 
    def test_update_place_without_token(self, client):
        """Modifier un logement sans token retourne 401."""
        place_id = _create_place(client, self.user_token, self.owner_id).get_json()['id']
        resp = client.put(f'/api/v1/places/{place_id}', json={
            "title": "X", "price": 10.0,
            "latitude": 0.0, "longitude": 0.0,
        })
        assert resp.status_code == 401
 
    def test_boundary_latitude_min(self, client):
        resp = _create_place(client, self.user_token, self.owner_id, latitude=-90.0)
        assert resp.status_code == 201
 
    def test_boundary_latitude_max(self, client):
        resp = _create_place(client, self.user_token, self.owner_id, latitude=90.0)
        assert resp.status_code == 201
 
    def test_boundary_longitude_min(self, client):
        resp = _create_place(client, self.user_token, self.owner_id, longitude=-180.0)
        assert resp.status_code == 201
 
    def test_boundary_longitude_max(self, client):
        resp = _create_place(client, self.user_token, self.owner_id, longitude=180.0)
        assert resp.status_code == 201
 
    def test_get_reviews_by_place_empty(self, client):
        """Liste de reviews vide pour un logement sans reviews."""
        place_id = _create_place(client, self.user_token, self.owner_id).get_json()['id']
        resp = client.get(f'/api/v1/places/{place_id}/reviews')
        assert resp.status_code == 200
        assert resp.get_json() == []
 
    def test_get_reviews_by_invalid_place(self, client):
        """Reviews d'un logement inexistant retourne 404."""
        resp = client.get('/api/v1/places/nonexistent-id/reviews')
        assert resp.status_code == 404
 
 
# ═════════════════════════════════════════════════════════════════════════════
# 5. REVIEWS
# ═════════════════════════════════════════════════════════════════════════════
 
class TestReviews:
 
    @pytest.fixture(autouse=True)
    def setup(self, client, admin_token, user_token):
        self.client = client
        self.admin_token = admin_token
        self.user_token, self.user_id = user_token
 
        # Créer un second user (propriétaire du logement)
        owner_resp = _create_user(client, admin_token,
                                   first_name="Owner", last_name="User",
                                   email="owner@hbnb.com", password="ownerpass123")
        self.owner_id = owner_resp.get_json()['id']
 
        owner_login = client.post('/api/v1/auth/login', json={
            "email": "owner@hbnb.com",
            "password": "ownerpass123"
        })
        self.owner_token = owner_login.get_json()['access_token']
 
        self.place_id = _create_place(
            client, self.owner_token, self.owner_id
        ).get_json()['id']
 
    def test_create_review_success(self, client):
        """Un user peut créer une review."""
        resp = _create_review(client, self.user_token,
                               self.place_id, self.user_id)
        assert resp.status_code == 201
        data = resp.get_json()
        assert 'id' in data
        assert data['rating'] == 5
 
    def test_create_review_without_token(self, client):
        """Créer une review sans token retourne 401."""
        resp = client.post('/api/v1/reviews/', json={
            "text": "Nice", "rating": 4,
            "place_id": self.place_id, "user_id": self.user_id,
        })
        assert resp.status_code == 401
 
    def test_create_review_invalid_place(self, client):
        """Review sur un logement inexistant retourne 400/404."""
        resp = _create_review(client, self.user_token,
                               "bad-place-id", self.user_id)
        assert resp.status_code in [400, 404]
 
    def test_create_review_invalid_user(self, client):
        """Review avec un user inexistant retourne 400/404."""
        resp = _create_review(client, self.user_token,
                               self.place_id, "bad-user-id")
        assert resp.status_code in [400, 404]
 
    def test_create_review_empty_text(self, client):
        """Review avec texte vide retourne 400."""
        resp = client.post('/api/v1/reviews/', json={
            "text": "", "rating": 3,
            "place_id": self.place_id, "user_id": self.user_id,
        }, headers=auth_headers(self.user_token))
        assert resp.status_code in [400, 422]
 
    def test_create_review_rating_too_high(self, client):
        """Rating > 5 retourne 400."""
        resp = client.post('/api/v1/reviews/', json={
            "text": "OK", "rating": 6,
            "place_id": self.place_id, "user_id": self.user_id,
        }, headers=auth_headers(self.user_token))
        assert resp.status_code in [400, 422]
 
    def test_create_review_rating_too_low(self, client):
        """Rating < 1 retourne 400."""
        resp = client.post('/api/v1/reviews/', json={
            "text": "OK", "rating": 0,
            "place_id": self.place_id, "user_id": self.user_id,
        }, headers=auth_headers(self.user_token))
        assert resp.status_code in [400, 422]
 
    def test_create_review_missing_rating(self, client):
        """Review sans rating retourne 400."""
        resp = client.post('/api/v1/reviews/', json={
            "text": "OK",
            "place_id": self.place_id, "user_id": self.user_id,
        }, headers=auth_headers(self.user_token))
        assert resp.status_code in [400, 422]
 
    def test_list_reviews_public(self, client):
        """Lister les reviews est public."""
        _create_review(client, self.user_token, self.place_id, self.user_id)
        resp = client.get('/api/v1/reviews/')
        assert resp.status_code == 200
        assert isinstance(resp.get_json(), list)
 
    def test_get_review_by_id(self, client):
        """Récupérer une review par son ID."""
        review_id = _create_review(client, self.user_token,
                                    self.place_id, self.user_id).get_json()['id']
        resp = client.get(f'/api/v1/reviews/{review_id}')
        assert resp.status_code == 200
        assert resp.get_json()['id'] == review_id
 
    def test_get_review_not_found(self, client):
        """Review inexistante retourne 404."""
        resp = client.get('/api/v1/reviews/nonexistent-id')
        assert resp.status_code == 404
 
    def test_update_review_as_author(self, client):
        """L'auteur peut modifier sa review."""
        review_id = _create_review(client, self.user_token,
                                    self.place_id, self.user_id).get_json()['id']
        resp = client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated text", "rating": 4,
            "place_id": self.place_id, "user_id": self.user_id,
        }, headers=auth_headers(self.user_token))
        assert resp.status_code == 200
        assert resp.get_json()['text'] == 'Updated text'
 
    def test_update_review_not_found(self, client):
        """Modifier une review inexistante retourne 404."""
        resp = client.put('/api/v1/reviews/nonexistent-id', json={
            "text": "X", "rating": 3,
            "place_id": self.place_id, "user_id": self.user_id,
        }, headers=auth_headers(self.user_token))
        assert resp.status_code == 404
 
    def test_update_review_without_token(self, client):
        """Modifier une review sans token retourne 401."""
        review_id = _create_review(client, self.user_token,
                                    self.place_id, self.user_id).get_json()['id']
        resp = client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "X", "rating": 3,
            "place_id": self.place_id, "user_id": self.user_id,
        })
        assert resp.status_code == 401
 
    def test_delete_review_as_author(self, client):
        """L'auteur peut supprimer sa review."""
        review_id = _create_review(client, self.user_token,
                                    self.place_id, self.user_id).get_json()['id']
        resp = client.delete(f'/api/v1/reviews/{review_id}',
                             headers=auth_headers(self.user_token))
        assert resp.status_code == 200
        assert client.get(f'/api/v1/reviews/{review_id}').status_code == 404
 
    def test_delete_review_as_admin(self, client):
        """Un admin peut supprimer n'importe quelle review."""
        review_id = _create_review(client, self.user_token,
                                    self.place_id, self.user_id).get_json()['id']
        resp = client.delete(f'/api/v1/reviews/{review_id}',
                             headers=auth_headers(self.admin_token))
        assert resp.status_code == 200
 
    def test_delete_review_not_found(self, client):
        """Supprimer une review inexistante retourne 404."""
        resp = client.delete('/api/v1/reviews/nonexistent-id',
                             headers=auth_headers(self.user_token))
        assert resp.status_code == 404
 
    def test_delete_review_without_token(self, client):
        """Supprimer une review sans token retourne 401."""
        review_id = _create_review(client, self.user_token,
                                    self.place_id, self.user_id).get_json()['id']
        resp = client.delete(f'/api/v1/reviews/{review_id}')
        assert resp.status_code == 401
 
    def test_get_reviews_by_place(self, client):
        """Récupérer les reviews d'un logement."""
        _create_review(client, self.user_token,
                        self.place_id, self.user_id, text="Nice", rating=4)
        resp = client.get(f'/api/v1/places/{self.place_id}/reviews')
        assert resp.status_code == 200
        reviews = resp.get_json()
        assert all(r['place_id'] == self.place_id for r in reviews)
 
    def test_get_reviews_by_invalid_place(self, client):
        """Reviews d'un logement inexistant retourne 404."""
        resp = client.get('/api/v1/places/nonexistent-id/reviews')
        assert resp.status_code == 404