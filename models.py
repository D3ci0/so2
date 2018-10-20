from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from geoalchemy2 import Geometry

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"] = ''
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Registrazione(db.Model):
    __tablename__ = 'registrazioni'

    idreg = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Text)
    nome = db.Column(db.Text)
    dettagli = db.Column(db.Text)
    prezzo = db.Column(db.Float)
    pos = db.Column(Geometry(geometry_type='POINT', srid=4326))
    data = db.Column(db.DateTime)
    idutente = db.Column(db.Integer, db.ForeignKey('utenti.idutente'))
    utente = db.relationship("Utente", back_populates = "idreg", lazy='joined')


    def __init__(self, nome, tipo, dettagli, prezzo, pos, data, idutente):
        self.nome = nome
        self.tipo = tipo
        self.dettagli = dettagli
        self.prezzo = prezzo
        self.pos = pos
        self.data = data
        self.idutente = idutente


class Utente(db.Model):
    __tablename__ = 'utenti'

    idutente = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    nome = db.Column(db.Text)
    cognome = db.Column(db.Text)
    idreg = db.relationship('Registrazione', back_populates = "utente")

    def __init__(self, nome, cognome, username, password):
        self.nome = nome
        self.cognome = cognome
        self.username = username
        self.password = password



class UtenteSchema(Schema):
    idutente = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    nome = fields.Str()
    cognome = fields.Str()

class RegistrazioneSchema(Schema):
    idreg = fields.Int(dump_only=True)
    nome = fields.Str()
    tipo = fields.Str()
    dettagli = fields.Str()
    prezzo = fields.Str()
    data = fields.Date()
    pos = fields.Str()
    idutente = fields.Str()
    utente = fields.Nested(UtenteSchema, allow_none=True)





utente_schema = UtenteSchema()
utenti_schema = UtenteSchema(many=True)
registrazione_schema = RegistrazioneSchema()
registrazioni_schema = RegistrazioneSchema(many=True)
