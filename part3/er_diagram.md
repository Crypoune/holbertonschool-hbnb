# HBnB — Entity-Relationship Diagram

## Database Schema

​```mermaid
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
​```