"""
Exécuter ce script pour générer :
  - le hash bcrypt du mot de passe admin
  - les UUIDs des amenities
  
Usage : python generate_seed_values.py
"""
import uuid
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# ── Hash du mot de passe admin ──
admin_password = "admin1234"
hashed = bcrypt.generate_password_hash(admin_password).decode("utf-8")
print(f"Admin password hash : {hashed}")

# ── UUIDs pour les amenities ──
amenities = ["WiFi", "Swimming Pool", "Air Conditioning"]
for name in amenities:
    print(f"{name} UUID : {uuid.uuid4()}")