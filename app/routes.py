from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from app.models import Etablissement, Classe, Enseignant, Eleve, ResultatAnnuel, Note, Absence, Matiere
from app import db

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

@main.route('/eleves')
@login_required
def gestion_eleves():
    eleves = Eleve.query.order_by(Eleve.nom).all()
    classes = Classe.query.order_by(Classe.nom).all()
    etablissements = Etablissement.query.order_by(Etablissement.nom).all()
    return render_template(
        'admin/eleves.html',
        eleves=eleves,
        classes=classes,
        etablissements=etablissements
    )

"Page de gestion des élèves, avec possibilité d'ajouter et de supprimer des élèves."
@main.route('/eleves/ajouter', methods=['POST'])
@login_required
def ajouter_eleve():
    matricule = request.form.get('matricule', '').strip()
    nom = request.form.get('nom', '').strip()
    prenom = request.form.get('prenom', '').strip()
    sexe = request.form.get('sexe', '')
    date_naissance = request.form.get('date_naissance') or None
    lieu_naissance = request.form.get('lieu_naissance', '').strip()
    adresse = request.form.get('adresse', '').strip()
    nom_parent = request.form.get('nom_parent', '').strip()
    telephone_parent = request.form.get('telephone_parent', '').strip()
    email_parent = request.form.get('email_parent', '').strip()
    statut = request.form.get('statut', 'actif')
    classe_id = request.form.get('classe_id')
    etablissement_id = request.form.get('etablissement_id')

    if not matricule or not nom or not prenom or not sexe or not classe_id or not etablissement_id:
        flash("Veuillez remplir tous les champs obligatoires.", "error")
        return redirect(url_for('main.gestion_eleves'))

    if Eleve.query.filter_by(matricule=matricule).first():
        flash("Ce matricule existe déjà.", "error")
        return redirect(url_for('main.gestion_eleves'))

    nouvel_eleve = Eleve(
        matricule=matricule,
        nom=nom,
        prenom=prenom,
        sexe=sexe,
        date_naissance=date_naissance,
        lieu_naissance=lieu_naissance,
        adresse=adresse,
        nom_parent=nom_parent,
        telephone_parent=telephone_parent,
        email_parent=email_parent,
        statut=statut,
        classe_id=classe_id,
        etablissement_id=etablissement_id
    )

    db.session.add(nouvel_eleve)
    db.session.commit()

    flash(f"Élève {prenom} {nom} ajouté avec succès.", "success")
    return redirect(url_for('main.gestion_eleves'))


@main.route('/eleves/supprimer/<int:eleve_id>', methods=['POST'])
@login_required
def supprimer_eleve(eleve_id):
    eleve = Eleve.query.get_or_404(eleve_id)
    nom_complet = f"{eleve.prenom} {eleve.nom}"

    db.session.delete(eleve)
    db.session.commit()

    flash(f"Élève {nom_complet} supprimé.", "success")
    return redirect(url_for('main.gestion_eleves'))

"Page de gestion des classes, avec possibilité d'ajouter et de supprimer des classes."
@main.route('/classes')
@login_required
def gestion_classes():
    classes = Classe.query.order_by(Classe.annee_scolaire.desc(), Classe.nom).all()
    etablissements = Etablissement.query.order_by(Etablissement.nom).all()
    return render_template(
        'admin/classes.html',
        classes=classes,
        etablissements=etablissements
    )


@main.route('/classes/ajouter', methods=['POST'])
@login_required
def ajouter_classe():
    nom = request.form.get('nom', '').strip()
    niveau = request.form.get('niveau', '').strip()
    filiere = request.form.get('filiere', '').strip()
    annee_scolaire = request.form.get('annee_scolaire', '').strip()
    effectif_max = request.form.get('effectif_max') or None
    etablissement_id = request.form.get('etablissement_id')

    if not nom or not niveau or not annee_scolaire or not etablissement_id:
        flash("Veuillez remplir tous les champs obligatoires.", "error")
        return redirect(url_for('main.gestion_classes'))

    nouvelle_classe = Classe(
        nom=nom,
        niveau=niveau,
        filiere=filiere,
        annee_scolaire=annee_scolaire,
        effectif_max=effectif_max,
        etablissement_id=etablissement_id
    )

    db.session.add(nouvelle_classe)
    db.session.commit()

    flash(f"Classe {nom} ajoutée avec succès.", "success")
    return redirect(url_for('main.gestion_classes'))


@main.route('/classes/supprimer/<int:classe_id>', methods=['POST'])
@login_required
def supprimer_classe(classe_id):
    classe = Classe.query.get_or_404(classe_id)

    if classe.eleves:
        flash(f"Impossible de supprimer {classe.nom} : des élèves y sont encore rattachés.", "error")
        return redirect(url_for('main.gestion_classes'))

    nom_classe = classe.nom
    db.session.delete(classe)
    db.session.commit()

    flash(f"Classe {nom_classe} supprimée.", "success")
    return redirect(url_for('main.gestion_classes'))

"Page de gestion des établissements, avec possibilité d'ajouter et de supprimer des établissements."
@main.route('/etablissements')
@login_required
def gestion_etablissements():
    etablissements = Etablissement.query.order_by(Etablissement.nom).all()
    return render_template('admin/etablissements.html', etablissements=etablissements)


@main.route('/etablissements/ajouter', methods=['POST'])
@login_required
def ajouter_etablissement():
    nom = request.form.get('nom', '').strip()
    type_etablissement = request.form.get('type_etablissement', '')
    zone = request.form.get('zone', '')
    ville = request.form.get('ville', '').strip()
    adresse = request.form.get('adresse', '').strip()
    telephone = request.form.get('telephone', '').strip()
    email = request.form.get('email', '').strip()

    if not nom or not type_etablissement or not zone:
        flash("Veuillez remplir tous les champs obligatoires.", "error")
        return redirect(url_for('main.gestion_etablissements'))

    nouvel_etablissement = Etablissement(
        nom=nom,
        type_etablissement=type_etablissement,
        zone=zone,
        ville=ville,
        adresse=adresse,
        telephone=telephone,
        email=email
    )

    db.session.add(nouvel_etablissement)
    db.session.commit()

    flash(f"Établissement {nom} ajouté avec succès.", "success")
    return redirect(url_for('main.gestion_etablissements'))


@main.route('/etablissements/supprimer/<int:etablissement_id>', methods=['POST'])
@login_required
def supprimer_etablissement(etablissement_id):
    etablissement = Etablissement.query.get_or_404(etablissement_id)

    if etablissement.classes or etablissement.enseignants or etablissement.eleves:
        flash(f"Impossible de supprimer {etablissement.nom} : des classes, enseignants ou élèves y sont encore rattachés.", "error")
        return redirect(url_for('main.gestion_etablissements'))

    nom_etablissement = etablissement.nom
    db.session.delete(etablissement)
    db.session.commit()

    flash(f"Établissement {nom_etablissement} supprimé.", "success")
    return redirect(url_for('main.gestion_etablissements'))