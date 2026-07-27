import os

from app import create_app, db
from app.models import User

app = create_app()
def creer_admin_par_defaut():
    """Crée un compte admin s'il n'en existe encore aucun."""
    admin_existant = User.query.filter_by(role='admin').first()

    if admin_existant is None:
        nom_utilisateur = os.environ.get('ADMIN_USERNAME')
        email = os.environ.get('ADMIN_EMAIL')
        mot_de_passe = os.environ.get('ADMIN_PASSWORD')

        admin = User(
            username=nom_utilisateur,
            email=email,
            role='admin'
        )
        admin.set_password(mot_de_passe)

        db.session.add(admin)
        db.session.commit()

        print(f"Compte admin créé automatiquement : {email} / {mot_de_passe}")
    else:
        print("Un compte admin existe déjà — aucune création nécessaire.")
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        creer_admin_par_defaut()
        
    app.run(debug=True)