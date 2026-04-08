-- seed_demo.sql
-- Peuple la base de données HBnB avec des données de démonstration.
-- À exécuter UNE SEULE FOIS après avoir initialisé la DB.

BEGIN TRANSACTION;

-- 1. Suppression des données existantes (pour éviter les doublons lors de multiples exécutions)
DELETE FROM place_amenity;
DELETE FROM reviews;
DELETE FROM places;
DELETE FROM amenities;
DELETE FROM users;

-- 2. Insertion des utilisateurs (avec UUIDs)
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password, is_admin)
VALUES
    ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$Sex64n/VkLaMb04LlSoj0eTGtEi0YQ13/XeE.YmVVBRj3pfvUuipu', TRUE),
    ('550e8400-e29b-41d4-a716-446655440001', 'Arnaud', 'Messenet', 'arnaud.messenet@hbnb.io', '$2b$12$qJ41T0sg2ebzmks1sxCiaeHkqnElp3U.ITIHqKF9VhyC.pdiDDl12', FALSE),
    ('550e8400-e29b-41d4-a716-446655440002', 'Thomas', 'Haenel', 'thomas.haenel@hbnb.io', '$2b$12$qJ41T0sg2ebzmks1sxCiaeHkqnElp3U.ITIHqKF9VhyC.pdiDDl12', FALSE),
    ('550e8400-e29b-41d4-a716-446655440003', 'David', 'Dufont', 'david.dufont@hbnb.io', '$2b$12$qJ41T0sg2ebzmks1sxCiaeHkqnElp3U.ITIHqKF9VhyC.pdiDDl12', FALSE);

-- 3. Insertion des équipements (amenities)
INSERT OR IGNORE INTO amenities (id, name)
VALUES
    ('6ba7b810-9dad-11d1-80b4-00c04fd430c8', 'WiFi'),
    ('6ba7b811-9dad-11d1-80b4-00c04fd430c8', 'Swimming Pool'),
    ('6ba7b812-9dad-11d1-80b4-00c04fd430c8', 'Air Conditioning'),
    ('6ba7b813-9dad-11d1-80b4-00c04fd430c8', 'Parking'),
    ('6ba7b814-9dad-11d1-80b4-00c04fd430c8', 'Kitchen');

-- 4. Insertion des lieux (places)
INSERT OR IGNORE INTO places (id, title, description, price, latitude, longitude, owner_id, image_url)
VALUES
    ('7ba7b810-9dad-11d1-80b4-00c04fd430c8', 'Cozy Studio in Paris', 'A charming studio in the heart of Paris, close to the Eiffel Tower.', 85.0, 48.8566, 2.3522, '550e8400-e29b-41d4-a716-446655440001', 'paris_studio.jpg'),
    ('7ba7b811-9dad-11d1-80b4-00c04fd430c8', 'Sunny Villa in Nice', 'Beautiful villa with a pool and sea view on the French Riviera.', 220.0, 43.7102, 7.2620, '550e8400-e29b-41d4-a716-446655440002', 'nice_villa.jpg'),
    ('7ba7b812-9dad-11d1-80b4-00c04fd430c8', 'Mountain Chalet in Chamonix', 'Cozy wooden chalet at the foot of Mont Blanc, perfect for skiing.', 150.0, 45.9237, 6.8694, '550e8400-e29b-41d4-a716-446655440003', 'chamonix_chalet.jpg'),
    ('7ba7b813-9dad-11d1-80b4-00c04fd430c8', 'Modern Loft in Lyon', 'Spacious loft in the Confluence district, close to restaurants and shops.', 70.0, 45.7640, 4.8357, '550e8400-e29b-41d4-a716-446655440001', 'lyon_loft.jpg'),
    ('7ba7b814-9dad-11d1-80b4-00c04fd430c8', 'Beachside Apartment in Biarritz', 'Steps from the beach, perfect for surfers and sea lovers.', 110.0, 43.4832, -1.5586, '550e8400-e29b-41d4-a716-446655440002', 'biarritz_apt.jpg');

-- 5. Insertion des avis (reviews)
INSERT OR IGNORE INTO reviews (id, text, rating, user_id, place_id)
VALUES
    ('8ba7b810-9dad-11d1-80b4-00c04fd430c8', 'Absolutely lovely place, very clean and well located!', 5, '550e8400-e29b-41d4-a716-446655440002', '7ba7b810-9dad-11d1-80b4-00c04fd430c8'),
    ('8ba7b811-9dad-11d1-80b4-00c04fd430c8', 'Great value for money, the host was very responsive.', 4, '550e8400-e29b-41d4-a716-446655440003', '7ba7b810-9dad-11d1-80b4-00c04fd430c8'),
    ('8ba7b812-9dad-11d1-80b4-00c04fd430c8', 'The villa is stunning, the pool was perfect.', 5, '550e8400-e29b-41d4-a716-446655440001', '7ba7b811-9dad-11d1-80b4-00c04fd430c8'),
    ('8ba7b813-9dad-11d1-80b4-00c04fd430c8', 'Magical place, we loved every minute of it.', 5, '550e8400-e29b-41d4-a716-446655440002', '7ba7b812-9dad-11d1-80b4-00c04fd430c8'),
    ('8ba7b814-9dad-11d1-80b4-00c04fd430c8', 'Very modern and comfortable, great location in Lyon.', 4, '550e8400-e29b-41d4-a716-446655440003', '7ba7b813-9dad-11d1-80b4-00c04fd430c8');

-- 6. Association des équipements aux lieux (place_amenity)
-- Exemple : Le studio parisien a WiFi, Parking et Kitchen
INSERT OR IGNORE INTO place_amenity (place_id, amenity_id)
VALUES
    ('7ba7b810-9dad-11d1-80b4-00c04fd430c8', '6ba7b810-9dad-11d1-80b4-00c04fd430c8'), -- WiFi
    ('7ba7b810-9dad-11d1-80b4-00c04fd430c8', '6ba7b813-9dad-11d1-80b4-00c04fd430c8'), -- Parking
    ('7ba7b810-9dad-11d1-80b4-00c04fd430c8', '6ba7b814-9dad-11d1-80b4-00c04fd430c8'), -- Kitchen

    ('7ba7b811-9dad-11d1-80b4-00c04fd430c8', '6ba7b810-9dad-11d1-80b4-00c04fd430c8'), -- WiFi
    ('7ba7b811-9dad-11d1-80b4-00c04fd430c8', '6ba7b811-9dad-11d1-80b4-00c04fd430c8'), -- Swimming Pool
    ('7ba7b811-9dad-11d1-80b4-00c04fd430c8', '6ba7b814-9dad-11d1-80b4-00c04fd430c8'), -- Kitchen

    ('7ba7b812-9dad-11d1-80b4-00c04fd430c8', '6ba7b810-9dad-11d1-80b4-00c04fd430c8'), -- WiFi
    ('7ba7b812-9dad-11d1-80b4-00c04fd430c8', '6ba7b813-9dad-11d1-80b4-00c04fd430c8'), -- Parking

    ('7ba7b813-9dad-11d1-80b4-00c04fd430c8', '6ba7b810-9dad-11d1-80b4-00c04fd430c8'), -- WiFi
    ('7ba7b813-9dad-11d1-80b4-00c04fd430c8', '6ba7b814-9dad-11d1-80b4-00c04fd430c8'), -- Kitchen

    ('7ba7b814-9dad-11d1-80b4-00c04fd430c8', '6ba7b810-9dad-11d1-80b4-00c04fd430c8'), -- WiFi
    ('7ba7b814-9dad-11d1-80b4-00c04fd430c8', '6ba7b814-9dad-11d1-80b4-00c04fd430c8'); -- Kitchen

COMMIT;

-- Affichage des résultats (optionnel)
SELECT '🎉 Demo data seeded successfully!' AS message;
SELECT '📋 Summary:' AS summary,
       (SELECT COUNT(*) FROM users WHERE email LIKE '%@hbnb.io') AS users_count,
       (SELECT COUNT(*) FROM amenities) AS amenities_count,
       (SELECT COUNT(*) FROM places) AS places_count,
       (SELECT COUNT(*) FROM reviews) AS reviews_count,
       (SELECT COUNT(*) FROM place_amenity) AS place_amenity_count;
