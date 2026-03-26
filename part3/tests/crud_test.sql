-- ============================================================
-- HBnB CRUD Test Operations
-- ============================================================
-- Ce script vérifie le bon fonctionnement du schéma
-- et des données insérées.
-- ============================================================


-- ══════════════════════════════════════════════════════════════
-- A. VÉRIFICATION DES DONNÉES INITIALES (SELECT)
-- ══════════════════════════════════════════════════════════════

-- A1. Vérifier que l'admin existe avec is_admin = TRUE et le mot de passe hashé
SELECT id, first_name, last_name, email, password
FROM users
WHERE email = 'admin@hbnb.io';
AND is_admin = TRUE

-- A2. Lister toutes les amenities
SELECT id, name FROM amenities;


-- ══════════════════════════════════════════════════════════════
-- B. TEST INSERT — Créer des données de test
-- ══════════════════════════════════════════════════════════════

-- B1. Créer un utilisateur normal
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '3fa85f64-5717-4562-b3fc-2c963f66afa6',
    'Arnaud',
    'Messenet',
    'arnaud@example.com',
    '$2b$12$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJK',
    FALSE
);

-- B2. Créer un deuxième utilisateur (pour les reviews)
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '4fa85f64-5717-4562-b3fc-2c963f66afa7',
    'Thomas',
    'Haenel',
    'thomas@example.com',
    '$2b$12$abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJK',
    FALSE
);

-- B3. Créer un lieu (place) avec Arnaud comme propriétaire
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    '1fa85f64-5717-4562-b3fc-2c963f66afa6',
    'Cozy Apartment in Paris',
    'A beautiful flat near the Eiffel Tower',
    120.50,
    48.8566,
    2.3522,
    '3fa85f64-5717-4562-b3fc-2c963f66afa6'  -- owner = Arnaud
);

-- B4. Créer une review (Thomas review le lieu d'Arnaud)
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    '2fa85f64-5717-4562-b3fc-2c963f66afa6',
    'Superbe appartement, très bien situé !',
    5,
    '4fa85f64-5717-4562-b3fc-2c963f66afa7',  -- user = Thomas
    '1fa85f64-5717-4562-b3fc-2c963f66afa6'   -- place = Cozy Apartment
);

-- B5. Associer des amenities au lieu (place_amenity)
INSERT INTO place_amenity (place_id, amenity_id)
VALUES
    ('1fa85f64-5717-4562-b3fc-2c963f66afa6', '6fa459ea-ee8a-4372-a567-0e02b2c3d479'),  -- WiFi
    ('1fa85f64-5717-4562-b3fc-2c963f66afa6', '8gc671gc-gg0c-4594-c789-2g24d4e5f691');  -- Air Conditioning


-- ══════════════════════════════════════════════════════════════
-- C. TEST SELECT — Lire les données avec jointures
-- ══════════════════════════════════════════════════════════════

-- C1. Lister tous les lieux avec le nom du propriétaire
SELECT
    p.id        AS place_id,
    p.title,
    p.price,
    u.first_name || ' ' || u.last_name AS owner_name,
    u.email     AS owner_email
FROM places p
JOIN users u ON p.owner_id = u.id;

-- C2. Lister les reviews d'un lieu avec le nom de l'auteur
SELECT
    r.id        AS review_id,
    r.text,
    r.rating,
    u.first_name || ' ' || u.last_name AS reviewer,
    p.title     AS place_title
FROM reviews r
JOIN users u  ON r.user_id  = u.id
JOIN places p ON r.place_id = p.id;

-- C3. Lister les amenities d'un lieu
SELECT
    p.title     AS place_title,
    a.name      AS amenity_name
FROM place_amenity pa
JOIN places    p ON pa.place_id   = p.id
JOIN amenities a ON pa.amenity_id = a.id;


-- ══════════════════════════════════════════════════════════════
-- D. TEST UPDATE — Modifier des données
-- ══════════════════════════════════════════════════════════════

-- D1. Modifier le titre d'un lieu
UPDATE places
SET title = 'Luxury Apartment in Paris', updated_at = CURRENT_TIMESTAMP
WHERE id = '1fa85f64-5717-4562-b3fc-2c963f66afa6';

-- D2. Vérifier la modification
SELECT id, title, updated_at FROM places
WHERE id = '1fa85f64-5717-4562-b3fc-2c963f66afa6';

-- D3. Modifier le rating d'une review
UPDATE reviews
SET rating = 4, text = 'Très bien mais un peu bruyant', updated_at = CURRENT_TIMESTAMP
WHERE id = '2fa85f64-5717-4562-b3fc-2c963f66afa6';

-- D4. Vérifier
SELECT id, text, rating FROM reviews
WHERE id = '2fa85f64-5717-4562-b3fc-2c963f66afa6';

-- D5. Modifier le nom d'une amenity
UPDATE amenities
SET name = 'High-Speed WiFi', updated_at = CURRENT_TIMESTAMP
WHERE id = '6fa459ea-ee8a-4372-a567-0e02b2c3d479';

-- D6. Vérifier
SELECT id, name FROM amenities
WHERE id = '6fa459ea-ee8a-4372-a567-0e02b2c3d479';


-- ══════════════════════════════════════════════════════════════
-- F. TEST DELETE — Supprimer des données
-- ══════════════════════════════════════════════════════════════

-- F1. Supprimer une association place_amenity
DELETE FROM place_amenity
WHERE place_id   = '1fa85f64-5717-4562-b3fc-2c963f66afa6'
  AND amenity_id = '8gc671gc-gg0c-4594-c789-2g24d4e5f691';

-- F2. Vérifier qu'il ne reste qu'une amenity liée
SELECT COUNT(*) AS remaining_amenities
FROM place_amenity
WHERE place_id = '1fa85f64-5717-4562-b3fc-2c963f66afa6';

-- F3. Supprimer une review
DELETE FROM reviews
WHERE id = '2fa85f64-5717-4562-b3fc-2c963f66afa6';

-- F4. Vérifier la suppression
SELECT COUNT(*) AS remaining_reviews FROM reviews;

-- F5. Supprimer un lieu → doit aussi supprimer ses reviews et place_amenity (CASCADE)
DELETE FROM places
WHERE id = '1fa85f64-5717-4562-b3fc-2c963f66afa6';

-- F6. Vérifier la suppression en cascade
SELECT COUNT(*) AS orphan_reviews FROM reviews
WHERE place_id = '1fa85f64-5717-4562-b3fc-2c963f66afa6';

SELECT COUNT(*) AS orphan_pa FROM place_amenity
WHERE place_id = '1fa85f64-5717-4562-b3fc-2c963f66afa6';


-- ══════════════════════════════════════════════════════════════
-- G. NETTOYAGE — Supprimer les données de test
-- ══════════════════════════════════════════════════════════════

DELETE FROM users WHERE id = '3fa85f64-5717-4562-b3fc-2c963f66afa6';
DELETE FROM users WHERE id = '4fa85f64-5717-4562-b3fc-2c963f66afa7';

-- Remettre le nom original de l'amenity WiFi
UPDATE amenities
SET name = 'WiFi', updated_at = CURRENT_TIMESTAMP
WHERE id = '6fa459ea-ee8a-4372-a567-0e02b2c3d479';

-- Vérification finale
SELECT '=== USERS ===' AS section;
SELECT id, first_name, last_name, email, is_admin FROM users;

SELECT '=== AMENITIES ===' AS section;
SELECT id, name FROM amenities;