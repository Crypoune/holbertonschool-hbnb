# 1. Générer le hash bcrypt et les UUIDs
python generate_seed_values.py

# 2. Mettre à jour seed.sql avec les vraies valeurs

# 3. Exécuter avec SQLite
sqlite3 instance/dev.db < schema.sql
sqlite3 instance/dev.db < seed.sql
sqlite3 instance/dev.db < crud_test.sql

# OU tout d'un coup
sqlite3 instance/dev.db < schema.sql && \
sqlite3 instance/dev.db < seed.sql && \
sqlite3 instance/dev.db < crud_test.sql


