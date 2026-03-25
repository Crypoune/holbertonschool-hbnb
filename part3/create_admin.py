from app import create_app, db
from app.services import facade

# On charge l'application pour avoir accès à la base de données
app = create_app('config.DevelopmentConfig')

with app.app_context():
    print("👑 --- OUTIL DE GESTION ADMINISTRATEUR --- 👑")
    email = input("Entrez l'email de l'administrateur : ")
    
    # 1. On cherche si cet utilisateur existe déjà
    user = facade.get_user_by_email(email)
    
    if user:
        # Si oui, on le "promeut" (on lui donne les droits Admin)
        if user.is_admin:
            print(f"⚡ L'utilisateur {email} est DÉJÀ un administrateur.")
        else:
            user.is_admin = True
            db.session.commit()
            print(f"✅ Succès ! L'utilisateur {email} a été promu Administrateur.")
    else:
        # Si non, on crée un tout nouveau compte Admin
        print(f"L'utilisateur {email} n'existe pas. Création d'un nouveau compte...")
        first_name = input("Prénom : ")
        last_name = input("Nom : ")
        password = input("Mot de passe : ")
        
        admin_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'password': password,
            'is_admin': True
        }
        
        try:
            facade.create_user(admin_data)
            print(f"✅ Succès ! Le Super-Admin {email} a été créé.")
        except Exception as e:
            print(f"❌ Erreur lors de la création : {e}")