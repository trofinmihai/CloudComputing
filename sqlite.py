import sqlite3
import requests
conn = sqlite3.connect('orar.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE obiecte
#               (id INTEGER PRIMARY KEY AUTOINCREMENT, nume text, profesor_titular text, nr_restantieri int)''')

# c.execute('''CREATE TABLE clase
#               (id INTEGER PRIMARY KEY AUTOINCREMENT, nume text, etaj int, nr_locuri int)''')

# c.execute('''CREATE TABLE orar
               # (id INTEGER PRIMARY KEY AUTOINCREMENT, grupa text, obiect text, clasa int, ziua text, ora int, profesor text)''')
r = requests.get("http://127.0.0.1:7001/show/" + 'A1')
print(r.json()['nr_elevi'])

# Insert a row of data
# c.execute("INSERT INTO grupe VALUES ('A1','26','8.78')")

# Save (commit) the changes
conn.commit()




# c.execute('SELECT * FROM pop WHERE qty = \'Mihai\'')

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()