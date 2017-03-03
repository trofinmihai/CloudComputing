from flask import Flask, url_for
import json
import sqlite3

conn = sqlite3.connect('grupe.db')
c = conn.cursor()

app = Flask(__name__)

@app.route('/')
def api_root():
    return 'Grupe de studenti'

@app.route('/add/<nume>/<nr_elevi>/<medie_clasa>')
def add_group(nume,nr_elevi,medie_clasa):

    #inseram in baza de date un rand nou
    new_entry = [(nume, nr_elevi, medie_clasa)]
    c.executemany("INSERT INTO grupe(nume, nr_elevi, medie_clasa) VALUES (?,?,?)", new_entry)
    conn.commit()
    # conn.close()
    # declarare dictionar
    data={}
    data['mesaj'] = "S-a introdus grupa" + nume

    # convertire din dictionar in JSON
    json_str = json.dumps(data)
    return json_str

@app.route('/show/<grupa>')
def show_group(grupa):
    #declaram dictionarul
    data = {}
    i = 0
    for row in c.execute("SELECT * FROM grupe where nume='%s'"%str(grupa)):
        data['grupa'] = list(row)[1]
        data['nr_elevi'] = list(row)[2]
        data['medie_clasa'] = list(row)[3]

    # convertire din dictionar in JSON
    json_str = json.dumps(data)
    return json_str

@app.route('/show')
def show_all_group():
    data = {}
    grupe = list()
    i = 0
    for row in c.execute("SELECT * FROM grupe"):
        data[i] = {"id":list(row)[0], "grupa":list(row)[1],"nr_elevi":list(row)[2], "medie_clasa":list(row)[3]}
        i += 1

    return json.dumps(data)

if __name__ == '__main__':
    app.run(port=7001)