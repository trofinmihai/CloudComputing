from flask import Flask, url_for
import requests
import json
import sqlite3

conn = sqlite3.connect('clase.db')
conn1 = sqlite3.connect('orar.db')
c = conn.cursor()
c1 = conn1.cursor()

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Clase si Orar'

@app.route('/add/clasa/<nume>/<etaj>/<nr_locuri>')
def add_clasa(nume, etaj, nr_locuri):
    data = {}
    # inseram in baza de date un rand nou
    new_entry = [(nume, etaj, nr_locuri)]
    c.executemany("INSERT INTO clase(nume, etaj, nr_locuri) VALUES (?,?,?)", new_entry)
    conn.commit()

    # declarare dictionar
    data = {}
    data['mesaj'] = "S-a introdus clasa " + nume

    # convertire din dictionar in JSON
    json_str = json.dumps(data)
    return json_str

@app.route('/show/<clasa>')
def show_clasa(clasa):
    #declaram dictionarul
    data = {}
    i = 0
    for row in c.execute("SELECT * FROM clase where nume='%d'"%int(clasa)):
        data['clasa'] = list(row)[1]
        data['etaj'] = list(row)[2]
        data['nr_locuri'] = list(row)[3]

    # convertire din dictionar in JSON
    json_str = json.dumps(data)
    return json_str

@app.route('/show')
def show_all_classes():
    data = {}
    grupe = list()
    i = 0
    for row in c.execute("SELECT * FROM clase"):
        data[i] = {"id":list(row)[0], "clasa":list(row)[1],"etaj":list(row)[2], "nr_locuri":list(row)[3]}
        i += 1
    return json.dumps(data)

@app.route('/show/orar')
def show_orar():
    data = {}

    i = 0
    for row in c1.execute("SELECT * FROM orar"):
        data[i] = list(row)
        i += 1
    return json.dumps(data)


@app.route('/add/orar/<grupa>/<clasa>/<obiect>/<zi>/<ora>')
def add_orar(grupa, obiect, clasa, zi, ora):

    data = {}

    r = requests.get("http://127.0.0.1:7001/show/" + str(grupa))
    p = requests.get("http://127.0.0.1:7002/show/" + str(obiect))
    # q = requests.get("http://127.0.0.1:7003/show/" + clasa)

    # return json.dumps(r.json())

    if(r.json()['nr_elevi']>30):
        data['error'] = "Nu sunt destule locuri in sala pentru aceasta grupa!"
        return json.dumps(data)


    new_entry = [(grupa, obiect, clasa, zi, ora, p.json()['profesor'])]
    c1.executemany("INSERT INTO orar(grupa, obiect, clasa, ziua, ora, profesor) VALUES (?,?,?,?,?,?)", new_entry)
    conn1.commit()

    data['mesaj'] = "O noua intrare in orar pentru grupa " + grupa + " a fost inregistrata."
    return json.dumps(data)


if __name__ == '__main__':
    app.run(port=7003)