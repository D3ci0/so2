import datetime
from flask import jsonify, request
from models import Registrazione, Utente, app, db, utenti_schema, registrazioni_schema, registrazione_schema, utente_schema
from geoalchemy2 import *
from pytz import timezone, utc

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
    registrazione = Registrazione.query.filter_by(idutente = idutente)
    if registrazione.count()>1 :
        result = registrazioni_schema.dump(registrazione)
    else :
        result = registrazione_schema.dump(registrazione)
    return jsonify(result.data)

@app.route('/save_reg', methods = ['POST'])
def save_reg():
    json = request.get_json()
    print(json)
    date = int(float(json['data']))
    data = datetime.datetime.fromtimestamp(date/1e3)
    europe = timezone('Europe/Rome')
    utctime = utc.localize(data)
    local_tz = utctime.astimezone(europe)
    print(local_tz)
    registrazione = Registrazione(json['nome'], json['tipo'], json['dettagli'], json['prezzo'], json['pos'], local_tz, json['idutente'])
    registrazione.pos = WKTElement(registrazione.pos, 4326)
    db.session.add(registrazione)
    db.session.commit()
    response = jsonify('Registration successfully saved')
    return response

@app.route('/auth_user', methods = ['GET','POST'])
def auth_user():
    json = request.get_json()
    username = json['username']
    password = json['password']
    utente = Utente.query.filter_by(username = username).first()
    if utente :
        if password == utente.password :
            result = utente_schema.dump(utente)
            return jsonify(result.data)
        else:
            wrongp = Utente('','',username,'')
            result = utente_schema.dump(wrongp)
            return jsonify(result.data)
    wrongu = Utente('','','','')
    result = utente_schema.dump(wrongu)
    return jsonify(result.data)

@app.route('/search_reg', methods = ['GET','POST'])
def search_reg():
    json = request.get_json()
    print(json)
    wkbpos = json['pos']
    range = json['range'] #nome = json['nome'],  fromdate = json['from'], todate = json['to']
    tipo = json['tipo']
    range =  (int(float(range))*1000)
    res = Registrazione.query
    if tipo is not None :
        res = res.filter_by(tipo = tipo)
    if wkbpos is not None and range is not None:
        res = res.filter(func.ST_Distance_Sphere(Registrazione.pos, wkbpos) < range)

    registrazione = res.all()
    if len(registrazione)> 1:
        result = registrazioni_schema.dump(registrazione)
    else :
        result = registrazione_schema.dump(registrazione)
    return jsonify(result.data)


if __name__ == '__main__':
        app.run()