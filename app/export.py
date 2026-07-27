import io
import zipfile
import pandas as pd
from flask import Blueprint, send_file
from flask_login import login_required
from app.models import (
    Etablissement, Classe, Enseignant, Eleve,
    Matiere, Note, Absence, ResultatAnnuel
)

export_bp = Blueprint('export', __name__)

# Ordre respectant les clés étrangères :
# chaque table n'apparaît qu'après les tables dont elle dépend
TABLES_A_EXPORTER = [
    ('etablissements', Etablissement),
    ('classes', Classe),          # dépend de etablissements
    ('enseignants', Enseignant),  # dépend de etablissements
    ('matieres', Matiere),
    ('eleves', Eleve),            # dépend de classes, etablissements
    ('notes', Note),              # dépend de eleves, matieres, enseignants
    ('absences', Absence),        # dépend de eleves
    ('resultats_annuels', ResultatAnnuel),  # dépend de eleves
]


def _modele_vers_dataframe(modele):
    """Convertit tous les enregistrements d'un modèle en DataFrame,
    en conservant toutes les colonnes, y compris les clés étrangères,
    pour que les relations entre tables restent exploitables."""
    colonnes = [colonne.name for colonne in modele.__table__.columns]
    lignes = modele.query.all()
    donnees = [
        {colonne: getattr(ligne, colonne) for colonne in colonnes}
        for ligne in lignes
    ]
    return pd.DataFrame(donnees, columns=colonnes)


@export_bp.route('/export/excel')
@login_required
def export_excel():
    """Un seul fichier .xlsx, une feuille par table."""
    tampon = io.BytesIO()

    with pd.ExcelWriter(tampon, engine='openpyxl') as ecrivain:
        for nom_feuille, modele in TABLES_A_EXPORTER:
            df = _modele_vers_dataframe(modele)
            df.to_excel(ecrivain, sheet_name=nom_feuille[:31], index=False)

    tampon.seek(0)
    return send_file(
        tampon,
        as_attachment=True,
        download_name='labo_academy_export.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


@export_bp.route('/export/csv')
@login_required
def export_csv():
    """Une archive ZIP contenant un fichier .csv par table."""
    tampon_zip = io.BytesIO()

    with zipfile.ZipFile(tampon_zip, 'w', zipfile.ZIP_DEFLATED) as archive:
        for nom_fichier, modele in TABLES_A_EXPORTER:
            df = _modele_vers_dataframe(modele)
            archive.writestr(f'{nom_fichier}.csv', df.to_csv(index=False))

    tampon_zip.seek(0)
    return send_file(
        tampon_zip,
        as_attachment=True,
        download_name='labo_academy_export_csv.zip',
        mimetype='application/zip'
    )