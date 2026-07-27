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
        'etablissements': Etablissement.query.count(),
        'classes': Classe.query.count(),
        'enseignants': Enseignant.query.count(),
        'eleves': Eleve.query.count(),
        'matieres': Matiere.query.count(),
        'notes': Note.query.count(),
        'absences': Absence.query.count(),
        'resultats': ResultatAnnuel.query.count(),
    }
    return render_template('admin/dashboard.html', stats=stats)