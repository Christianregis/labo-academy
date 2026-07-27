from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app import db
from app.models import User

auth = Blueprint('auth', __name__)


@auth.route('/inscription', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        # Validations de base
        if not username or not email or not password:
            flash("Tous les champs sont obligatoires.", "error")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash("Un compte existe déjà avec cet email.", "error")
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash("Ce nom d'utilisateur est déjà pris.", "error")
            return redirect(url_for('auth.register'))

        nouvel_utilisateur = User(username=username, email=email)
        nouvel_utilisateur.set_password(password)

        db.session.add(nouvel_utilisateur)
        db.session.commit()

        flash("Compte créé avec succès. Vous pouvez vous connecter.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')


@auth.route('/connexion', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        utilisateur = User.query.filter_by(email=email).first()

        if utilisateur is None or not utilisateur.check_password(password):
            flash("Email ou mot de passe incorrect.", "error")
            print(f"{utilisateur}")
            return redirect(url_for('auth.login'))

        login_user(utilisateur)
        
        if utilisateur.role == 'admin':
            flash(f"Bienvenue, {utilisateur.username} (Administrateur) !", "success")
            return redirect(url_for('main.dashboard'))
        else:
            flash(f"Bienvenue, {utilisateur.username} (Utilisateur) !", "success")
            return redirect(url_for('main.index'))

    return render_template('login.html')


@auth.route('/deconnexion')
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.", "success")
    return redirect(url_for('auth.login'))