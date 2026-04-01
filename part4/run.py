from app import create_app, db

app = create_app('config.DevelopmentConfig')

with app.app_context():
    # Crée toutes les tables SQLAlchemy si elles n'existent pas
    db.create_all()

if __name__ == '__main__':
    print("🚀 Running on http://127.0.0.1:5000/api/v1/")
    app.run(debug=True)