from flask_bcrypt import generate_password_hash

passwords = {
    "admin1234": None,
    "password123": None,
}

for plain_password, _ in passwords.items():
    hashed_password = generate_password_hash(plain_password).decode('utf-8')
    passwords[plain_password] = hashed_password
    print(f"Mot de passe '{plain_password}' hachÃ© : {hashed_password}")
