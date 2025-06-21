from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Tournoi, Joueur, Match, Prix
from app.forms import TournoiForm, JoueurForm, MatchForm, ResultatMatchForm, PrixForm

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    tournois = Tournoi.query.order_by(Tournoi.date_debut.desc()).limit(5).all()
    return render_template('index.html', tournois=tournois)

# CRUD Tournois
@bp.route('/tournois')
@login_required
def list_tournois():
    tournois = Tournoi.query.filter_by(user_id=current_user.id).all()
    return render_template('tournois/list.html', tournois=tournois)

@bp.route('/tournois/create', methods=['GET', 'POST'])
@login_required
def create_tournoi():
    form = TournoiForm()
    if form.validate_on_submit():
        tournoi = Tournoi(
            nom=form.nom.data,
            jeu=form.jeu.data,
            date_debut=form.date_debut.data,
            date_fin=form.date_fin.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(tournoi)
        db.session.commit()
        flash('Tournoi créé avec succès!', 'success')
        return redirect(url_for('main.list_tournois'))
    return render_template('tournois/create.html', form=form)

@bp.route('/tournois/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_tournoi(id):
    tournoi = Tournoi.query.get_or_404(id)
    if tournoi.organisateur != current_user:
        flash('Vous n\'avez pas la permission de modifier ce tournoi', 'danger')
        return redirect(url_for('main.list_tournois'))
    
    form = TournoiForm(obj=tournoi)
    if form.validate_on_submit():
        tournoi.nom = form.nom.data
        tournoi.jeu = form.jeu.data
        tournoi.date_debut = form.date_debut.data
        tournoi.date_fin = form.date_fin.data
        tournoi.description = form.description.data
        db.session.commit()
        flash('Tournoi mis à jour avec succès!', 'success')
        return redirect(url_for('main.list_tournois'))
    return render_template('tournois/edit.html', form=form, tournoi=tournoi)

@bp.route('/tournois/<int:id>/delete', methods=['POST'])
@login_required
def delete_tournoi(id):
    tournoi = Tournoi.query.get_or_404(id)
    if tournoi.organisateur != current_user:
        flash('Vous n\'avez pas la permission de supprimer ce tournoi', 'danger')
        return redirect(url_for('main.list_tournois'))
    
    db.session.delete(tournoi)
    db.session.commit()
    flash('Tournoi supprimé avec succès!', 'success')
    return redirect(url_for('main.list_tournois'))

@bp.route('/tournois/<int:id>')
@login_required
def detail_tournoi(id):
    tournoi = Tournoi.query.get_or_404(id)
    return render_template('tournois/detail.html', tournoi=tournoi)

# CRUD Joueurs
@bp.route('/joueurs')
@login_required
def list_joueurs():
    joueurs = Joueur.query.all()
    return render_template('joueurs/list.html', joueurs=joueurs)

@bp.route('/joueurs/create', methods=['GET', 'POST'])
@login_required
def create_joueur():
    form = JoueurForm()
    if form.validate_on_submit():
        joueur = Joueur(
            pseudo=form.pseudo.data,
            nom_complet=form.nom_complet.data,
            email=form.email.data
        )
        db.session.add(joueur)
        db.session.commit()
        flash('Joueur ajouté avec succès!', 'success')
        return redirect(url_for('main.list_joueurs'))
    return render_template('joueurs/create.html', form=form)

@bp.route('/joueurs/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_joueur(id):
    joueur = Joueur.query.get_or_404(id)
    form = JoueurForm(obj=joueur)
    if form.validate_on_submit():
        joueur.pseudo = form.pseudo.data
        joueur.nom_complet = form.nom_complet.data
        joueur.email = form.email.data
        db.session.commit()
        flash('Joueur mis à jour avec succès!', 'success')
        return redirect(url_for('main.list_joueurs'))
    return render_template('joueurs/edit.html', form=form, joueur=joueur)

@bp.route('/joueurs/<int:id>/delete', methods=['POST'])
@login_required
def delete_joueur(id):
    joueur = Joueur.query.get_or_404(id)
    db.session.delete(joueur)
    db.session.commit()
    flash('Joueur supprimé avec succès!', 'success')
    return redirect(url_for('main.list_joueurs'))

# CRUD Matchs
@bp.route('/matchs')
@login_required
def list_matchs():
    matchs = Match.query.all()
    return render_template('matchs/list.html', matchs=matchs)

@bp.route('/matchs/create', methods=['GET', 'POST'])
@login_required
def create_match():
    form = MatchForm()
    form.tournoi.choices = [(t.id, t.nom) for t in Tournoi.query.all()]
    form.joueur1.choices = [(j.id, j.pseudo) for j in Joueur.query.all()]
    form.joueur2.choices = [(j.id, j.pseudo) for j in Joueur.query.all()]
    
    if form.validate_on_submit():
        match = Match(
            tournoi_id=form.tournoi.data,
            joueur1_id=form.joueur1.data,
            joueur2_id=form.joueur2.data,
            date_match=form.date_match.data
        )
        db.session.add(match)
        db.session.commit()
        flash('Match programmé avec succès!', 'success')
        return redirect(url_for('main.list_matchs'))
    return render_template('matchs/create.html', form=form)

@bp.route('/matchs/<int:id>/result', methods=['GET', 'POST'])
@login_required
def result_match(id):
    match = Match.query.get_or_404(id)
    form = ResultatMatchForm()
    if form.validate_on_submit():
        match.score_joueur1 = form.score_joueur1.data
        match.score_joueur2 = form.score_joueur2.data
        match.termine = True
        db.session.commit()
        flash('Résultat enregistré avec succès!', 'success')
        return redirect(url_for('main.list_matchs'))
    return render_template('matchs/result.html', form=form, match=match)

# CRUD Prix
@bp.route('/tournois/<int:tournoi_id>/prix')
@login_required
def list_prix(tournoi_id):
    tournoi = Tournoi.query.get_or_404(tournoi_id)
    return render_template('prix/list.html', tournoi=tournoi)

@bp.route('/tournois/<int:tournoi_id>/prix/create', methods=['GET', 'POST'])
@login_required
def create_prix(tournoi_id):
    tournoi = Tournoi.query.get_or_404(tournoi_id)  # Récupère le tournoi
    form = PrixForm()
    if form.validate_on_submit():
        if form.position.data <= 0:
            flash("La position doit être un nombre positif", 'danger')
            return render_template('prix/create.html', form=form, tournoi=tournoi)
        else:
        
            prix = Prix(
                tournoi_id=tournoi_id,
                position=form.position.data,
                montant=form.montant.data,
                description=form.description.data
            )
            db.session.add(prix)
            db.session.commit()
            flash('Prix ajouté avec succès!', 'success')
            return redirect(url_for('main.list_prix', tournoi_id=tournoi_id))
    return render_template('prix/create.html', form=form, tournoi=tournoi)  # Ajoutez tournoi ici
@bp.route('/prix/<int:prix_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_prix(prix_id):
    prix = Prix.query.get_or_404(prix_id)
    tournoi = prix.tournoi  # Récupère automatiquement le tournoi associé
    form = PrixForm(obj=prix)  # Pré-remplit le formulaire avec les données existantes

    if form.validate_on_submit():
        if form.position.data <= 0:
            flash("La position doit être un nombre positif", 'danger')
            return render_template('prix/edit.html', form=form, prix=prix, tournoi=tournoi)
        
        prix.position = form.position.data
        prix.montant = form.montant.data
        prix.description = form.description.data
        db.session.commit()
        flash('Prix modifié avec succès!', 'success')
        return redirect(url_for('main.list_prix', tournoi_id=tournoi.id))

    return render_template('prix/edit.html', form=form, prix=prix, tournoi=tournoi)
@bp.route('/prix/<int:prix_id>/delete', methods=['POST'])
@login_required
def delete_prix(prix_id):
    prix = Prix.query.get_or_404(prix_id)
    tournoi_id = prix.tournoi.id
    db.session.delete(prix)
    db.session.commit()
    flash('Prix supprimé avec succès!', 'success')
    return redirect(url_for('main.list_prix', tournoi_id=tournoi_id))
# Recherche et Filtrage
# @bp.route('/search')
# def search():
#     query = request.args.get('q', '')
#     if query:
#         tournois = Tournoi.query.filter(Tournoi.nom.ilike(f'%{query}%')).all()
#         joueurs = Joueur.query.filter(Joueur.pseudo.ilike(f'%{query}%')).all()
#     else:
#         tournois = []
#         joueurs = []
#     return render_template('search.html', tournois=tournois, joueurs=joueurs, query=query)

# amelioration recherche 
@bp.route('/search')
def search():
    query = request.args.get('q', '').strip()
    
    tournois = []
    joueurs = []
    
    if query:
        # Recherche insensible à la casse et partielle
        search_filter = f"%{query}%"

        tournois = Tournoi.query.filter(
            Tournoi.nom.ilike(search_filter) | 
            Tournoi.jeu.ilike(search_filter)
        ).order_by(Tournoi.date_debut.desc()).all()

        joueurs = Joueur.query.filter(
            Joueur.pseudo.ilike(search_filter) |
            Joueur.nom_complet.ilike(search_filter)
        ).order_by(Joueur.pseudo).all()

    return render_template('search.html',tournois=tournois,joueurs=joueurs,query=query)