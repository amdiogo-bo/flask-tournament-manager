import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'une-cle-secrete-tres-secure'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:passer@localhost:5432/tournois_gaming_db?client_encoding=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False