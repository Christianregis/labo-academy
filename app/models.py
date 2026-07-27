from app import db
from flask_login import UserMixin
from datetime import datetime, date


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='utilisateur')  # admin / utilisateur
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)


class Etablissement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    type_etablissement = db.Column(db.String(20), nullable=False)   # public / privé
    zone = db.Column(db.String(20), nullable=False)                 # rural / urbain
    ville = db.Column(db.String(100))
    adresse = db.Column(db.String(255))
    telephone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    classes = db.relationship('Classe', backref='etablissement', lazy=True)
    enseignants = db.relationship('Enseignant', backref='etablissement', lazy=True)
    eleves = db.relationship('Eleve', backref='etablissement', lazy=True)


class Classe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)          # ex: 6e A, Terminale D
    niveau = db.Column(db.String(50), nullable=False)       # ex: 6e, 5e, Terminale
    filiere = db.Column(db.String(50))                      # ex: Scientifique, Littéraire
    annee_scolaire = db.Column(db.String(9), nullable=False)  # ex: 2025-2026
    effectif_max = db.Column(db.Integer)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), nullable=False)

    eleves = db.relationship('Eleve', backref='classe', lazy=True)


class Enseignant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(30), unique=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    sexe = db.Column(db.String(1), nullable=False)          # M / F
    matiere_principale = db.Column(db.String(80))
    telephone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    date_embauche = db.Column(db.Date)
    statut = db.Column(db.String(20), default='actif')      # actif / inactif
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), nullable=False)


class Eleve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(30), unique=True, nullable=False)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    sexe = db.Column(db.String(1), nullable=False)          # M / F
    date_naissance = db.Column(db.Date)
    lieu_naissance = db.Column(db.String(100))
    adresse = db.Column(db.String(255))
    nom_parent = db.Column(db.String(120))
    telephone_parent = db.Column(db.String(30))
    email_parent = db.Column(db.String(120))
    date_inscription = db.Column(db.Date, default=date.today)
    statut = db.Column(db.String(20), default='actif')      # actif / transféré / abandon
    classe_id = db.Column(db.Integer, db.ForeignKey('classe.id'), nullable=False)
    etablissement_id = db.Column(db.Integer, db.ForeignKey('etablissement.id'), nullable=False)

    notes = db.relationship('Note', backref='eleve', lazy=True)
    absences = db.relationship('Absence', backref='eleve', lazy=True)
    resultats = db.relationship('ResultatAnnuel', backref='eleve', lazy=True)


class Matiere(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    coefficient = db.Column(db.Float, default=1.0)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    matiere_id = db.Column(db.Integer, db.ForeignKey('matiere.id'), nullable=False)
    enseignant_id = db.Column(db.Integer, db.ForeignKey('enseignant.id'))
    type_evaluation = db.Column(db.String(30), nullable=False)  # devoir / interrogation / examen
    valeur = db.Column(db.Float, nullable=False)
    note_sur = db.Column(db.Float, default=20.0)
    trimestre = db.Column(db.String(20), nullable=False)         # Trimestre 1 / 2 / 3
    annee_scolaire = db.Column(db.String(9), nullable=False)
    date_evaluation = db.Column(db.Date, default=date.today)

    matiere = db.relationship('Matiere')
    enseignant = db.relationship('Enseignant')


class Absence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    date_absence = db.Column(db.Date, nullable=False, default=date.today)
    duree_heures = db.Column(db.Float, default=1.0)
    justifiee = db.Column(db.Boolean, default=False)
    motif = db.Column(db.String(255))
    trimestre = db.Column(db.String(20))
    annee_scolaire = db.Column(db.String(9), nullable=False)


class ResultatAnnuel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eleve_id = db.Column(db.Integer, db.ForeignKey('eleve.id'), nullable=False)
    annee_scolaire = db.Column(db.String(9), nullable=False)
    moyenne_generale = db.Column(db.Float)
    rang = db.Column(db.Integer)
    resultat_final = db.Column(db.String(20))   # admis / redouble / échec
    mention = db.Column(db.String(30))
    date_deliberation = db.Column(db.Date)