# Ejemplo de aplicación Flask con un formulario de login. El usuario y la contraseña se consultan de una base de datos SQLite.
# El usuario se almacena en una variable de sesión.
# Se utiliza el decorador @login_required para proteger la ruta /home
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    if 'username' in session:
        #return "Bienvenido a la aplicación, " + session['username']
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']
        # Comprobar si el usuario existe en la base de datos
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        # Esto es un ejemplo de cómo NO debería hacerse: concatenando los valores de los parámetros en la consulta
        cur.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'")

        # Así es como debería hacerse: parametrizando la consulta
        # cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))

        user = cur.fetchone()
        conn.close()
        # Si el usuario existe, almacenar el usuario en una variable de sesión y redirigir a la página home
        if user:
            session['username'] = user[0]
            return redirect(url_for('index'))
        else:
            error = 'Usuario o contraseña incorrectos'
    return render_template('login.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/clients')
def clients():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM clients')
    clients = cur.fetchall()
    clients = [dict(id=row[0], name=row[1], address=row[2], city=row[3], zip_code=row[4], phone=row[5], email=row[6]) for row in clients]
    conn.close()
    return render_template('clients.html', clients=clients, username=session.get('username', None))


@app.route('/clients/<int:id>', methods=['GET','POST'])
def client_detail(id):
    if request.method == 'POST':
        if 'save' in request.form:
            name = request.form['name']
            address = request.form['address']
            city = request.form['city']
            zip_code = request.form['zip_code']
            phone = request.form['phone']
            email = request.form['email']
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute('UPDATE clients SET name=?, address=?, city=?, zip_code=?, phone=?, email=? WHERE id=?', (name, address, city, zip_code, phone, email, id))
            conn.commit()
            conn.close()
            return redirect(url_for('clients'))
        elif 'delete' in request.form:
            conn = sqlite3.connect('database.db')
            cur = conn.cursor()
            cur.execute('DELETE FROM clients WHERE id=?', (id,))
            conn.commit()
            conn.close()
            return redirect(url_for('clients'))
    else:
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        # Forma incorrecta:
        cur.execute("SELECT * FROM clients WHERE id = " + str(id))
        # Forma correcta:
        #cur.execute('SELECT * FROM clients WHERE id = ?', (id,))
        client = cur.fetchone()
        client = dict(id=client[0], name=client[1], address=client[2], city=client[3], zip_code=client[4], phone=client[5], email=client[6])
        conn.close()
        return render_template('client_edit.html', client=client, username=session.get('username', None))


@app.route('/clients/new', methods=['GET','POST'])
def client_create():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        zip_code = request.form['zip_code']
        phone = request.form['phone']
        email = request.form['email']
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()
        cur.execute('INSERT INTO clients (name, address, city, zip_code, phone, email) VALUES (?,?,?,?,?,?)', (name, address, city, zip_code, phone, email))
        conn.commit()
        conn.close()
        return redirect(url_for('clients'))
    return render_template('client_edit.html', client={}, username=session.get('username', None))