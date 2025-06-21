from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    tournois = db.relationship('Tournoi', backref='organisateur', lazy=True)

class Tournoi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    jeu = db.Column(db.String(100), nullable=False)
    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    matchs = db.relationship('Match', backref='tournoi', lazy=True)
    prix = db.relationship('Prix', backref='tournoi', lazy=True)

class Joueur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(50), unique=True, nullable=False)
    nom_complet = db.Column(db.String(100))
    email = db.Column(db.String(120))
    matchs_joueur1 = db.relationship('Match', foreign_keys='Match.joueur1_id', backref='joueur1', lazy=True)
    matchs_joueur2 = db.relationship('Match', foreign_keys='Match.joueur2_id', backref='joueur2', lazy=True)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournoi_id = db.Column(db.Integer, db.ForeignKey('tournoi.id'), nullable=False)
    joueur1_id = db.Column(db.Integer, db.ForeignKey('joueur.id'), nullable=False)
    joueur2_id = db.Column(db.Integer, db.ForeignKey('joueur.id'), nullable=False)
    score_joueur1 = db.Column(db.Integer)
    score_joueur2 = db.Column(db.Integer)
    date_match = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    termine = db.Column(db.Boolean, default=False)

class Prix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournoi_id = db.Column(db.Integer, db.ForeignKey('tournoi.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    montant = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))