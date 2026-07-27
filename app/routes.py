from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Etablissement, Classe, Enseignant, Eleve, ResultatAnnuel, Note, Absence, Matiere

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login')
def login():
    return render_template('login.html')

@main.route('/register')
def register():
    return render_template('register.html')

@main.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'etablissements': 6,
        'classes': 4,
        'enseignants': 12,
        'eleves': 120,
        'matieres': 8,
        'notes': 480,
        'absences': 24,
        'resultats': 10,
    }
    return render_template('admin/dashboard.html', stats=stats)