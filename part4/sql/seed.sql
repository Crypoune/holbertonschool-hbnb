-- ============================================================
-- HBnB Initial Data Seed
-- ============================================================
-- Ce script insère les données initiales :
--   - 1 utilisateur administrateur
--   - 3 amenities de base
--
--   Le hash du mot de passe a été généré avec bcrypt2
--     via : python generate_seed_values.py
-- ============================================================



-- ──────────────────────────────────────────────────────────────
-- Administrateur
-- ──────────────────────────────────────────────────────────────

INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$FMHNBWKXZl0I1xcBkqvJa..Oi4njZL9jgYDLjjV2x7TydbY6IzgjS',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- ──────────────────────────────────────────────────────────────
-- Amenities initiales
-- ──────────────────────────────────────────────────────────────
-- Les UUIDs ont été générés via uuid.uuid4()
-- ──────────────────────────────────────────────────────────────

INSERT INTO amenities (id, name, created_at, updated_at)
VALUES
    ('8ec2e67d-cd19-412e-b887-7db137b89b8e',
     'WiFi',
     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

    ('9266428d-6ef5-4956-9c4c-36dfd69d2c99',
     'Swimming Pool',
     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

    ('75990514-b1f5-41a3-996e-e7214056e5fd',
     'Air Conditioning',
     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);