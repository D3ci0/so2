from flask import Flask, jsonify, request
from models import Registrazione, Utente, app, db, utenti_schema, registrazioni_schema, registrazione_schema, utente_schema
from geoalchemy2 import *

@app.route('/users', methods = ['GET'])
def get_all_users():
    utenti = Utente.query.all()
    result = utenti_schema.dump(utenti)
    return jsonify( result.data)

@app.route('/registrations', methods = ['GET'])
def get_all_registrations():
    registrazioni = Registrazione.query.all()
    result = registrazioni_schema.dump(registrazioni)
    return jsonify(result.data)

@app.route('/reg_by_user', methods = ['GET','POST'])
def get_reg_by_user():
    idutente = request.get_json()
    registrazione = Registrazione.query.filter_by(idutente = idutente).first()
    result = registrazione_schema.dump(registrazione)
    return jsonify(result.data)

@app.route('/save_reg', methods = ['POST'])
def save_reg():
    json = request.get_json()
    registrazione = Registrazione(json['nome'], json['tipo'], json['dettagli'], json['prezzo'], json['point'], json['data'], json['idutente'])
    registrazione.pos = WKTElement(registrazione.pos, 4326)
    db.session.add(registrazione)
    db.session.commit()
    response = jsonify({'Registration successfully saved'})
    response.status_code = 200
    return response

@app.route('/auth_user', methods = ['GET','POST'])
def auth_user():
    json = request.get_json()
    print(json)
    username = json['username']
    password = json['password']
    utente = Utente.query.filter_by(username = username).first()
    if utente :
        if password == utente.password :
            result = utente_schema.dump(utente)
            return jsonify(result.data)
        else:
            wrongp = jsonify({'Wrong password'})
            wrongp.status_code = 404
            return wrongp
    wrongu = jsonify({'Wrong username'})
    wrongu.status_code = 404
    return wrongu



if __name__ == '__main__':
        app.run()