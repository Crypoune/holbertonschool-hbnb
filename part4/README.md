# HolbertonBnB (HBnB) — Part 4: Simple Web Client

A simplified AirBnB clone with a fully functional web client built in HTML5, CSS3, and JavaScript ES6. The frontend connects to the RESTful API secured with JWT authentication and backed by a persistent SQLite database. Built with Python, Flask, Flask-RESTx, SQLAlchemy, Flask-JWT-Extended, and Flask-CORS, the project follows a modular three-tier architecture that cleanly separates presentation, business logic, and persistence concerns.

---

## Table of Contents

1. [Project Architecture](#project-architecture)
2. [Layered Architecture](#layered-architecture)
3. [Database Schema](#database-schema)
4. [Quick Start](#quick-start)
5. [Features](#features)
6. [API Endpoints](#api-endpoints)
7. [Authentication & Authorization](#authentication--authorization)
8. [Frontend Web Client](#frontend-web-client)
9. [Code Walkthrough](#code-walkthrough)
10. [Design Patterns](#design-patterns)
11. [Testing](#testing)
12. [Technical Glossary](#technical-glossary)
13. [Resources](#resources)
14. [Authors](#authors)

---

## Project Architecture

```
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── amenities.py                 # Amenity endpoints (admin-only writes)
│   │   │   ├── auth.py                      # JWT login endpoint + protected test route
│   │   │   ├── places.py                    # Place endpoints (JWT-protected writes)
│   │   │   ├── reviews.py                   # Review endpoints (JWT-protected writes)
│   │   │   └── users.py                     # User endpoints (admin-only creation)
│   │   └── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── amenity.py                       # Amenity model — many-to-many with Place
│   │   ├── base_model.py                    # Abstract SQLAlchemy base — id, timestamps
│   │   ├── place.py                         # Place model — GPS validation, owner FK
│   │   ├── review.py                        # Review model — rating 1–5, user/place FKs
│   │   └── user.py                          # User model — bcrypt hashing, email validation
│   ├── persistence/
│   │   ├── __init__.py
│   │   └── repository.py                    # ABC Repository + SQLAlchemyRepository
│   ├── services/
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── amenity_repository.py        # AmenityRepository
│   │   │   ├── place_repository.py          # PlaceRepository
│   │   │   ├── review_repository.py         # ReviewRepository — get_reviews_by_place()
│   │   │   └── user_repository.py           # UserRepository — get_user_by_email()
│   │   ├── __init__.py                      # Singleton: facade = HBnBFacade()
│   │   └── facade.py                        # HBnBFacade — orchestrator
│   └── __init__.py                          # Application Factory — create_app(), db, bcrypt, jwt, CORS
├── frontend/
│   ├── images/
│   │   ├── amenities/                       # Amenity icons
│   │   └── places/                          # Place photos
│   ├── scripts/
│   │   ├── auth/
│   │   │   ├── cookie.js                    # Gestion des cookies
│   │   │   └── login.js                     # Logique de login/logout
│   │   ├── places/
│   │   │   ├── index.js                     # Logique de la page d'accueil (liste des places)
│   │   │   └── place.js                     # Logique de la page de détail d'une place
│   │   ├── reviews/
│   │   │   ├── reviewForm.js                # Logique du formulaire d'ajout de review (inline)
│   │   │   └── addReview.js                 # Logique de la page dédiée à l'ajout de review
│   │   ├── shared/
│   │   │   ├── header.js                    # Logique du header (auth, etc.)
│   │   │   └── utils.js                     # Fonctions utilitaires partagées
│   │   └── main.js                          # Point d'entrée principal
│   ├── add_reviews.html                     # Add review form (authenticated only)
│   ├── index.html                           # Main page — list of places
│   ├── login.html                           # Login form
│   ├── place.html                           # Place details + inline review form
│   ├── register.html                        # Registration form (bonus)
│   ├── scripts.js                           # All client-side JS logic
│   ├── styles.css                           # Global stylesheet
│   └── README.md                            # Frontend documentation
├── sql/
│   ├── schema.sql                           # Raw SQL — full database schema
│   └── seed.sql                             # Raw SQL — initial data (admin + amenities)
├── tests/
│   ├── crud_test.sql
│   └── test_hbnb_api.py                     # Full test suite — JWT, Users, Places, Reviews, Amenities
├── .gitignore
├── config.py                                # Environment-based configuration (Dev / Prod)
├── requirements.txt                         # Python dependencies
└── run.py                                   # Application entry point
```

---

## Layered Architecture

The application strictly follows a **Three-Tier Architecture** where each layer has a single, clearly defined responsibility.

```
+---------------------------------------------+
|         PRESENTATION LAYER (API)            |
|  app/api/v1/  ->  Flask-RESTx Namespaces    |
|  JWT validation via @jwt_required()         |
+--------------------+------------------------+
                     | calls
+--------------------v------------------------+
|             FACADE (HBnBFacade)             |
|  app/services/facade.py                     |
|  Single entry point — Singleton             |
+--------------------+------------------------+
                     | calls
+--------------------v------------------------+
|       BUSINESS LOGIC LAYER (Models)        |
|  app/models/  ->  User, Place, Review...   |
|  Business rules, bcrypt, GPS validation    |
+--------------------+------------------------+
                     | calls
+--------------------v------------------------+
|       PERSISTENCE LAYER (Repository)       |
|  SQLAlchemyRepository + entity repos       |
|  SQLite (dev) — MySQL-ready (prod)         |
+---------------------------------------------+
```

**Essential flow:**

```
HTTP Request → JWT middleware → API (flask-restx) → Facade → Model / Repository → JSON Response
```

### Layer responsibilities

| Layer          | Folder                     | Responsibility                                            | Does NOT know about  |
| -------------- | -------------------------- | --------------------------------------------------------- | -------------------- |
| Presentation   | `app/api/v1/`              | Receive HTTP, validate JWT, validate payload, return JSON | How data is stored   |
| Business Logic | `app/models/`              | Business rules, entity validation, bcrypt, relationships  | Flask, HTTP, storage |
| Persistence    | `app/persistence/` + repos | Store and retrieve data via SQLAlchemy                    | Business rules, API  |

---

## Database Schema

The following ER diagram represents the full database structure, including all entities, attributes, and relationships.

```mermaid
erDiagram
    USER ||--o{ PLACE : "owns"
    USER ||--o{ REVIEW : "writes"
    PLACE ||--o{ REVIEW : "receives"
    PLACE ||--o{ PLACE_AMENITY : "has"
    AMENITY ||--o{ PLACE_AMENITY : "belongs to"

    USER {
        CHAR_36 id PK
        VARCHAR_255 first_name
        VARCHAR_255 last_name
        VARCHAR_255 email
        VARCHAR_255 password
        BOOLEAN is_admin
    }

    PLACE {
        CHAR_36 id PK
        VARCHAR_255 title
        TEXT description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        CHAR_36 owner_id FK
    }

    REVIEW {
        CHAR_36 id PK
        TEXT text
        INT rating
        CHAR_36 user_id FK
        CHAR_36 place_id FK
    }

    AMENITY {
        CHAR_36 id PK
        VARCHAR_255 name
    }

    PLACE_AMENITY {
        CHAR_36 place_id FK
        CHAR_36 amenity_id FK
    }
```

### Relationships

| Relationship    | Type         | Description                        |
| --------------- | ------------ | ---------------------------------- |
| User → Place    | One-to-Many  | A user can own many places         |
| User → Review   | One-to-Many  | A user can write many reviews      |
| Place → Review  | One-to-Many  | A place can receive many reviews   |
| Place ↔ Amenity | Many-to-Many | Via the `place_amenity` join table |

---

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb/part4/
   ```

2. **Set up a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python3 run.py
```

The API will be available at:

- **API Base URL**: `http://127.0.0.1:5000/api/v1/`
- **Interactive Swagger Documentation**: `http://127.0.0.1:5000/api/v1/`

### Running the Frontend

Open the `frontend/` folder with the **Live Server** extension in VS Code, or open `frontend/index.html` directly in your browser.

> **Note**: Use `http://127.0.0.1:5500` consistently — the API URL in `scripts.js` is set to `http://127.0.0.1:5000`. Mixing `localhost` and `127.0.0.1` causes cookie issues.

### Initializing the Database

Run the SQL scripts to create the schema and populate demo data:

```bash
sqlite3 instance/dev.db < sql/schema.sql
sqlite3 instance/dev.db < sql/seed.sql
```

The `seed.sql` file includes:

- An admin user (`admin@hbnb.io` / `admin1234`)
- Demo users, places, reviews, and amenities with place-amenity associations

> To regenerate bcrypt hashes for the seed file, use `generate_seed_values.py`.

### Environment Variables

| Variable       | Default              | Description               |
| -------------- | -------------------- | ------------------------- |
| `SECRET_KEY`   | `default_secret_key` | Flask and JWT signing key |
| `DATABASE_URL` | `sqlite:///dev.db`   | Database URI              |

For production, set these in your environment:

```bash
export SECRET_KEY="your-strong-secret-key"
export DATABASE_URL="mysql://user:password@host/dbname"
```

### Running the Tests

```bash
python -m pytest tests/test_hbnb_api.py -v
```

### Dependencies

```
flask>=2.0.0
flask-restx>=1.0.0
flask-sqlalchemy>=3.0.0
flask-bcrypt>=1.0.0
flask-jwt-extended>=4.0.0
flask-cors>=4.0.0
```

---

## Features

### Core Functionality

- **User Management**: Create, read, and update users with email validation and bcrypt password hashing
- **Place Management**: Properties with GPS coordinates, pricing, owner FK, and linked amenities
- **Review System**: User reviews with ratings (1–5) for places, full CRUD including DELETE
- **Amenity Management**: Configurable amenities with many-to-many relationship to places

### Security Features

- **JWT Authentication**: Stateless token-based authentication via `flask-jwt-extended`
- **Password Hashing**: bcrypt hashing — passwords are never stored in plaintext or returned in responses
- **Role-Based Access Control (RBAC)**: `is_admin` claim embedded in JWT token
- **Ownership Validation**: Users can only modify their own places and reviews
- **Admin Privileges**: Admins bypass ownership restrictions and can manage all resources

### Technical Features

- **SQLAlchemy ORM**: Full database persistence replacing in-memory storage
- **SQLite for development**: Zero-configuration local database
- **MySQL-ready for production**: Switch via `DATABASE_URL` environment variable
- **Two-Level Validation**: Format validation at API layer + business rule validation at model layer
- **Repository Pattern**: Swappable persistence layer — `SQLAlchemyRepository` implements the same interface as the former `InMemoryRepository`
- **Auto-generated Documentation**: Interactive Swagger/OpenAPI UI at the root URL
- **CORS**: Flask-CORS configured to allow requests from the frontend dev server

### Frontend Features

- **Login / Logout**: JWT token stored in a cookie — header updates dynamically between Login and Logout
- **Place Listing**: Fetches all places from the API and displays them as cards with title, price, and image
- **Client-Side Price Filter**: Filter places by max price without reloading the page
- **Place Details**: Fetches place details, amenities, and reviews — enriches reviews with user names
- **Inline Review Form**: Authenticated users can submit a review directly on the place page
- **Add Review Page**: Standalone review form on `add_reviews.html` — redirects to index if not authenticated
- **Registration** _(bonus)_: `register.html` allows new users to create an account

---

## API Endpoints

The Swagger UI is available at `http://localhost:5000/api/v1/` and allows testing all endpoints interactively. Protected endpoints require a `Bearer <token>` in the `Authorization` header.

### Authentication `/api/v1/auth/`

| Method | URL                      | Auth required | Description                    |
| ------ | ------------------------ | ------------- | ------------------------------ |
| `POST` | `/api/v1/auth/login`     | ❌            | Login and receive JWT token    |
| `GET`  | `/api/v1/auth/protected` | ✅            | Test endpoint — verifies token |

**Example — POST /api/v1/auth/login**

```json
// Request body:
{
  "email": "admin@hbnb.io",
  "password": "admin1234"
}

// Response 200:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Users `/api/v1/users/`

| Method | URL                  | Auth required | Role           | Description    |
| ------ | -------------------- | ------------- | -------------- | -------------- |
| `POST` | `/api/v1/users/`     | ✅            | Admin only     | Create a user  |
| `GET`  | `/api/v1/users/`     | ❌            | Public         | List all users |
| `GET`  | `/api/v1/users/<id>` | ❌            | Public         | Get user by ID |
| `PUT`  | `/api/v1/users/<id>` | ✅            | Owner or Admin | Update a user  |

**Example — POST /api/v1/users/** _(admin token required)_

```json
// Request body:
{
  "first_name": "Arnaud",
  "last_name": "Messenet",
  "email": "arnaud.messenet@example.com",
  "password": "password123"
}

// Response 201:
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "first_name": "Arnaud",
  "last_name": "Messenet",
  "email": "arnaud.messenet@example.com",
  "is_admin": false
}
```

> Note: `password` is never returned in any response.

**Authorization rules for PUT /api/v1/users/\<id\>:**

- A regular user can only update their own `first_name` and `last_name`
- A regular user **cannot** modify `email` or `password` → `400`
- An admin can update any field of any user

---

### Places `/api/v1/places/`

| Method | URL                   | Auth required | Role           | Description                        |
| ------ | --------------------- | ------------- | -------------- | ---------------------------------- |
| `POST` | `/api/v1/places/`     | ✅            | Any user       | Create a place                     |
| `GET`  | `/api/v1/places/`     | ❌            | Public         | List all places                    |
| `GET`  | `/api/v1/places/<id>` | ❌            | Public         | Get place with owner and amenities |
| `PUT`  | `/api/v1/places/<id>` | ✅            | Owner or Admin | Update a place                     |

> Validation: `price > 0`, `latitude` in `[-90, 90]`, `longitude` in `[-180, 180]`.

---

### Reviews `/api/v1/reviews/`

| Method   | URL                           | Auth required | Role            | Description             |
| -------- | ----------------------------- | ------------- | --------------- | ----------------------- |
| `POST`   | `/api/v1/reviews/`            | ✅            | Any user        | Create a review         |
| `GET`    | `/api/v1/reviews/`            | ❌            | Public          | List all reviews        |
| `GET`    | `/api/v1/reviews/<id>`        | ❌            | Public          | Get a review by ID      |
| `PUT`    | `/api/v1/reviews/<id>`        | ✅            | Author or Admin | Update a review         |
| `DELETE` | `/api/v1/reviews/<id>`        | ✅            | Author or Admin | Delete a review         |
| `GET`    | `/api/v1/places/<id>/reviews` | ❌            | Public          | All reviews for a place |

> Validation: `text` cannot be empty, `rating` must be between 1 and 5 inclusive.

---

### Amenities `/api/v1/amenities/`

| Method | URL                      | Auth required | Role       | Description          |
| ------ | ------------------------ | ------------- | ---------- | -------------------- |
| `POST` | `/api/v1/amenities/`     | ✅            | Admin only | Create an amenity    |
| `GET`  | `/api/v1/amenities/`     | ❌            | Public     | List all amenities   |
| `GET`  | `/api/v1/amenities/<id>` | ❌            | Public     | Get an amenity by ID |
| `PUT`  | `/api/v1/amenities/<id>` | ✅            | Admin only | Update an amenity    |

---

### HTTP Status Codes

| Code | Meaning      | When used                                       |
| ---- | ------------ | ----------------------------------------------- |
| 200  | Success      | Successful GET, PUT, DELETE                     |
| 201  | Created      | Successful POST                                 |
| 400  | Bad Request  | Missing/invalid data, or business rule violated |
| 401  | Unauthorized | Missing or invalid JWT token                    |
| 403  | Forbidden    | Valid token but insufficient permissions        |
| 404  | Not Found    | Unknown UUID                                    |

---

## Authentication & Authorization

### JWT Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant JWTManager

    Client->>+API: POST /api/v1/auth/login (email, password)
    API->>+JWTManager: Validate credentials and generate JWT
    JWTManager-->>-API: Returns JWT token
    API-->>-Client: Returns JWT token in response

    Client->>+API: PUT /api/v1/places/<id> (Authorization: Bearer JWT)
    API->>+JWTManager: Validate JWT token
    JWTManager-->>-API: Valid token + claims (user_id, is_admin)
    API-->>-Client: Protected data response
```

### Token Claims

The JWT token embeds two claims:

- `identity` — the user's UUID
- `is_admin` — boolean flag for admin privileges

```python
access_token = create_access_token(
    identity=str(user.id),
    additional_claims={"is_admin": user.is_admin}
)
```

### Role-Based Access Control (RBAC)

| Action                                 | Regular User | Admin |
| -------------------------------------- | ------------ | ----- |
| Create user                            | ❌           | ✅    |
| Update own profile (name only)         | ✅           | ✅    |
| Update any user (incl. email/password) | ❌           | ✅    |
| Create/update own place                | ✅           | ✅    |
| Update any place                       | ❌           | ✅    |
| Create review (not own place)          | ✅           | ✅    |
| Update/delete own review               | ✅           | ✅    |
| Update/delete any review               | ❌           | ✅    |
| Create/update amenity                  | ❌           | ✅    |

---

## Frontend Web Client

The frontend is a pure HTML5/CSS3/JavaScript ES6 client served from the `frontend/` folder. It communicates with the Flask API via the Fetch API and manages authentication through JWT cookies.

### Pages

| Page           | File               | Auth required    | Description                                                      |
| -------------- | ------------------ | ---------------- | ---------------------------------------------------------------- |
| List of Places | `index.html`       | ❌               | Displays all places with price filter                            |
| Login          | `login.html`       | ❌               | JWT login form — redirects to index on success                   |
| Place Details  | `place.html`       | ❌ (form hidden) | Place info, amenities, reviews + inline review form              |
| Add Review     | `add_reviews.html` | ✅               | Standalone review form — redirects to index if not authenticated |
| Register       | `register.html`    | ❌               | _(bonus)_ New user registration                                  |

### Authentication Flow

```
1. User submits login form
2. JS sends POST to /api/v1/auth/login
3. API returns { access_token: "..." }
4. JS stores token in cookie (SameSite=Lax, 7 days)
5. All subsequent API calls include Authorization: Bearer <token>
6. Header button switches from "Login" to "Logout"
7. On logout: cookie is deleted, redirect to index
```

### Key JavaScript Functions

| Function                     | Description                                  |
| ---------------------------- | -------------------------------------------- |
| `getCookie(name)`            | Reads a cookie value by name                 |
| `setCookie(name, value)`     | Stores a cookie with 7-day expiry            |
| `isAuthenticated()`          | Returns true if JWT cookie exists            |
| `setupHeaderAuth()`          | Switches Login ↔ Logout in header            |
| `fetchPlaces()`              | GET all places from API                      |
| `setupPriceFilter()`         | Client-side price filtering                  |
| `fetchPlaceDetails(placeId)` | GET place + reviews + user names in parallel |
| `setupReviewForm(placeId)`   | Wires inline review form submission          |
| `initAddReviewPage()`        | Handles `add_reviews.html` auth + submission |

### CORS Configuration

The API is configured to accept requests from the frontend dev server:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5500", "http://127.0.0.1:5500"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
    }
})
```

---

## Code Walkthrough

### `config.py` — Configuration

```python
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    JWT_SECRET_KEY = SECRET_KEY

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

`JWT_SECRET_KEY` reuses `SECRET_KEY` — one environment variable controls both Flask session security and JWT signing. `SQLALCHEMY_DATABASE_URI` can be overridden via `DATABASE_URL` to switch from SQLite to MySQL without touching the code.

---

### `app/__init__.py` — Application Factory

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.url_map.strict_slashes = False
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": [...]}})
    # ... namespace registration
    return app
```

Four extensions are initialized here: `bcrypt` for password hashing, `jwt` for token management, `db` for ORM, and `CORS` to allow the frontend dev server to communicate with the API. `strict_slashes = False` prevents Flask from redirecting `/api/v1/places` to `/api/v1/places/`, which would strip the Authorization header and cause 401 errors on the frontend.

---

### `app/persistence/repository.py` — Repository & SQLAlchemyRepository

```python
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return db.session.get(self.model, obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
```

`SQLAlchemyRepository` implements the same `Repository` ABC as the former `InMemoryRepository`. The Facade and API layer required **zero changes** to switch from RAM to database — only the concrete implementation was swapped. This is the **Open/Closed Principle** in action.

---

### `app/models/base_model.py` — SQLAlchemy Base

```python
from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
```

`__abstract__ = True` tells SQLAlchemy not to create a table for `BaseModel` itself — only concrete subclasses get tables. `id` uses a UUID4 lambda as default, generated at insert time. `onupdate=datetime.now` automatically refreshes `updated_at` on every `UPDATE` statement.

---

### `app/models/user.py` — User Model

```python
class User(BaseModel):
    __tablename__ = 'users'

    _first_name = db.Column('first_name', db.String(50), nullable=False)
    _last_name  = db.Column('last_name',  db.String(50), nullable=False)
    _email      = db.Column('email',      db.String(120), nullable=False, unique=True)
    _password   = db.Column('password',   db.String(128), nullable=False)
    is_admin    = db.Column(db.Boolean, default=False)

    @password.setter
    def password(self, value):
        if not value.startswith(("$2a$", "$2b$", "$2y$")):
            self._password = bcrypt.generate_password_hash(value).decode("utf-8")
        else:
            self._password = value

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)
```

Private attributes (`_email`, `_password`) map to clean column names via `db.Column('email', ...)`. The `password` setter auto-detects if a value is already a bcrypt hash — preventing double-hashing. `verify_password` uses `bcrypt.check_password_hash` for constant-time comparison, resistant to timing attacks.

---

### `app/api/v1/auth.py` — Authentication Endpoint

```python
@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        credentials = api.payload or {}
        email = credentials.get('email')
        password = credentials.get('password')
        if not email or not password:
            return {'error': 'Email and password are required'}, 400

        user = facade.get_user_by_email(email)
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"is_admin": user.is_admin}
        )
        return {'access_token': access_token}, 200
```

`.get()` instead of `[]` for payload access prevents `KeyError` on missing fields. The same `401` is returned whether the email doesn't exist or the password is wrong — this prevents **user enumeration** attacks. The `is_admin` claim is embedded directly in the token, avoiding a database lookup on every protected request.

---

### `app/services/repositories/user_repository.py` — UserRepository

```python
class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(_email=email).first()
```

`UserRepository` extends `SQLAlchemyRepository` with one user-specific method. Note the use of `_email` — since the Python attribute is named `_email` (private by convention), SQLAlchemy's `filter_by` must use `_email`, not `email`. The database column name (`email`) is separate from the Python attribute name.

---

## Design Patterns

| Pattern                 | Where used                                                  | What it solves                                                                  |
| ----------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Facade**              | `app/services/facade.py`                                    | Single simplified interface to all business operations                          |
| **Repository**          | `app/persistence/repository.py`                             | Abstracts storage — swap InMemory for SQLAlchemy without touching API or models |
| **Singleton**           | `app/services/__init__.py`                                  | One shared `HBnBFacade` instance across the entire application                  |
| **Application Factory** | `app/__init__.py`                                           | Creates Flask app inside `create_app()` — different configs for dev/prod/test   |
| **ABC / Interface**     | `app/persistence/repository.py`, `app/models/base_model.py` | Enforces contracts via `@abstractmethod`                                        |
| **JWT Middleware**      | `@jwt_required()` decorator                                 | Intercepts requests and validates tokens before reaching route handlers         |
| **RBAC**                | `get_jwt()` claims in endpoints                             | Role-based access without querying the database on every request                |

---

## Testing

Tests use **pytest** and the **Flask test client**. No real server is launched — `app.test_client()` simulates HTTP requests in process. A fresh SQLite file database is created and destroyed for every test function, guaranteeing full isolation.

```python
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_hbnb.db'
    JWT_SECRET_KEY = 'test-secret-key-must-be-at-least-32-chars!!'

@pytest.fixture(scope='function')
def app():
    application = create_app()
    application.config.from_object(TestConfig)
    with application.app_context():
        db.create_all()
        import app.services as services_module
        from app.services.facade import HBnBFacade
        services_module.facade = HBnBFacade()  # Fresh facade for each test
        yield application
        db.session.remove()
        db.drop_all()
    if os.path.exists('instance/test_hbnb.db'):
        os.remove('instance/test_hbnb.db')
```

The facade is **re-instantiated** inside the fixture to ensure it points to the test database session, not the production one.

### Test structure

| Class           | What is tested                                                                                                                  |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `TestAuth`      | Login success/failure, missing fields, protected endpoint with/without/invalid token                                            |
| `TestUsers`     | Admin-only creation, 401 without token, 403 as regular user, duplicate email, password not exposed, owner vs admin update rules |
| `TestAmenities` | Admin-only writes, public reads, 404 on unknown ID                                                                              |
| `TestPlaces`    | JWT-protected creation, GPS boundary values, public reads, owner vs admin update                                                |
| `TestReviews`   | JWT-protected CRUD, rating validation, author vs admin delete, reviews by place                                                 |

### Test identities

| User                | Email              | Role in tests                          |
| ------------------- | ------------------ | -------------------------------------- |
| **Admin**           | `admin@hbnb.com`   | Created via fixture — owns admin token |
| **Arnaud Messenet** | `regular@hbnb.com` | Regular user — owns user token         |
| **Owner**           | `owner@hbnb.com`   | Place owner in review tests            |

### Example — cURL

```bash
# Login as admin (seeded by seed.sql)
curl -X POST http://127.0.0.1:5000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@hbnb.io", "password": "admin1234"}'

# Create a place (authenticated)
curl -X POST http://localhost:5000/api/v1/places/ \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{"title": "Cozy Flat", "price": 80.0, "latitude": 48.8, "longitude": 2.3, "owner_id": "<user_id>"}'

# List all places (public)
curl -X GET http://localhost:5000/api/v1/places/
```

---

## Technical Glossary

| Term                                 | Definition                                                                                                                                    |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **ABC (Abstract Base Class)**        | Python class defining a contract via `@abstractmethod`. Cannot be instantiated directly.                                                      |
| **Application Factory**              | Flask pattern where the app is created in `create_app()`, enabling multiple configurations.                                                   |
| **bcrypt**                           | Adaptive password hashing algorithm. Resistant to brute force due to configurable work factor.                                                |
| **CRUD**                             | Create, Read, Update, Delete — maps to POST, GET, PUT/PATCH, DELETE.                                                                          |
| **DRY (Don't Repeat Yourself)**      | Common code written once and inherited — applied via `BaseModel`.                                                                             |
| **Encapsulation**                    | Hiding internal details behind a simple interface — e.g., `_password` + `@property`.                                                          |
| **Facade Pattern**                   | Simplified interface to a complex system — `HBnBFacade` hides repositories.                                                                   |
| **JWT (JSON Web Token)**             | Stateless authentication token. Contains signed claims (user id, is_admin) — no server session needed.                                        |
| **Middleware**                       | Code that runs between receiving a request and handling it — `@jwt_required()` acts as JWT middleware.                                        |
| **ORM (Object-Relational Mapping)**  | Maps Python classes to database tables — SQLAlchemy handles SQL generation automatically.                                                     |
| **RBAC (Role-Based Access Control)** | Access control based on user roles — regular user vs admin, enforced via `is_admin` JWT claim.                                                |
| **Repository Pattern**               | Abstracts data access behind a generic interface — swap storage without changing business logic.                                              |
| **REST**                             | Representational State Transfer — HTTP-based, stateless, resource-oriented API style.                                                         |
| **Singleton**                        | One single instance throughout the app — `facade = HBnBFacade()` in `services/__init__.py`.                                                   |
| **SQLAlchemy**                       | Python ORM — maps classes to SQL tables, manages sessions and relationships.                                                                  |
| **Three-Tier Architecture**          | Presentation / Business Logic / Persistence — each layer has one responsibility.                                                              |
| **Two-Level Validation**             | Level 1: flask-restx validates format. Level 2: model validates business rules → `ValueError` → HTTP 400.                                     |
| **User Enumeration**                 | Security attack inferring valid emails from different error messages. Prevented by returning the same 401 for wrong email and wrong password. |
| **UUID4**                            | Random 128-bit identifier — generated via `str(uuid.uuid4())`. Globally unique, enumeration-resistant.                                        |

---

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/en/stable/)
- [Flask-Bcrypt Documentation](https://flask-bcrypt.readthedocs.io/en/latest/)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/en/latest/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/en/3.x/)
- [Mermaid.js Documentation](https://mermaid-js.github.io/mermaid/)
- [JWT.io](https://jwt.io/)
- [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
- [Handling Cookies in JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [REST API Best Practices](https://restfulapi.net/)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html)

---

## Known Limitations & Future Improvements

- **Registration**: User creation is currently restricted to administrators via the Swagger UI. A public registration request system — where users submit a request that an admin approves — could be implemented in a future version.
- **Admin Dashboard**: A dedicated frontend UI for managing places, users, and amenities without Swagger is a natural next step but was out of scope for this iteration.
- **Place Images**: Images are currently stored as filenames referencing local files. A future version could support file upload or external URLs.
- **Token Refresh**: JWT tokens expire after 15 minutes by default. Implementing a refresh token mechanism would improve the user experience.

---

## Authors

- [Arnaud Messenet](https://github.com/Crypoune) &nbsp;&nbsp; [![Badge](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/Crypoune)
- [Thomas Haenel](https://github.com/yorichill) &nbsp;&nbsp; [![Badge](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/yorichill)

---
