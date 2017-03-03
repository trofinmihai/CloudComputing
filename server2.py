from flask import Flask, url_for
import json
import math
import sqlite3

conn = sqlite3.connect('obiecte.db')
c = conn.cursor()

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Obiecte de facultate (cursuri si seminarii)'

@app.route('/add/<nume>/<profesor_titular>/<nr_restantieri>')
def add_object(nume,profesor_titular,nr_restantieri):

    #inseram in baza de date un rand nou
    new_entry = [(nume, profesor_titular, nr_restantieri)]
    c.executemany("INSERT INTO obiecte(nume, profesor_titular, nr_restantieri) VALUES (?,?,?)", new_entry)
    conn.commit()

    # declarare dictionar
    data={}
    data['mesaj'] = "S-a introdus obiectul " + nume

    # convertire din dictionar in JSON
    json_str = json.dumps(data)
    return json_str

@app.route('/show/<obiect>')
def show_obiect(obiect):
    #declaram dictionarul
    data = {}
    i = 0
    for row in c.execute("SELECT * FROM obiecte where nume='%s'"%str(obiect)):
        data['obiect'] = list(row)[1]
        data['profesor'] = list(row)[2]
        data['restantieri'] = list(row)[3]

    # convertire din dictionar in JSON
    json_str = json.dumps(data)
    return json_str

@app.route('/show')
def show_all_objects():
    data = {}
    grupe = list()
    i = 0
    for row in c.execute("SELECT * FROM obiecte"):
        data[i] = {"id":list(row)[0], "obiect":list(row)[1],"profesor":list(row)[2], "restantieri":list(row)[3]}
        i += 1

    return json.dumps(data)

if __name__ == '__main__':
    app.run(port=7002)