from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, TextAreaField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')

class RegistrationForm(FlaskForm):
    username = StringField('Nom d\'utilisateur', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris. Veuillez en choisir un autre.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé. Veuillez en choisir un autre.')

class TournoiForm(FlaskForm):
    nom = StringField('Nom du tournoi', validators=[DataRequired()])
    jeu = StringField('Jeu', validators=[DataRequired()])
    date_debut = DateTimeField('Date de début', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    date_fin = DateTimeField('Date de fin', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Créer')

class JoueurForm(FlaskForm):
    pseudo = StringField('Pseudo', validators=[DataRequired()])
    nom_complet = StringField('Nom complet')
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Ajouter')

class MatchForm(FlaskForm):
    tournoi = SelectField('Tournoi', coerce=int, validators=[DataRequired()])
    joueur1 = SelectField('Joueur 1', coerce=int, validators=[DataRequired()])
    joueur2 = SelectField('Joueur 2', coerce=int, validators=[DataRequired()])
    date_match = DateTimeField('Date du match', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
    submit = SubmitField('Programmer')

class ResultatMatchForm(FlaskForm):
    score_joueur1 = IntegerField('Score Joueur 1', validators=[DataRequired()])
    score_joueur2 = IntegerField('Score Joueur 2', validators=[DataRequired()])
    submit = SubmitField('Enregistrer')

class PrixForm(FlaskForm):
    position = IntegerField('Position', validators=[DataRequired()])
    montant = FloatField('Montant', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Ajouter')