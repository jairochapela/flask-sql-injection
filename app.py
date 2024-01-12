# Ejemplo de aplicación Flask con un formulario de login. El usuario y la contraseña se consultan de una base de datos SQLite.
# El usuario se almacena en una variable de sesión.
# Se utiliza el decorador @login_required para proteger la ruta /home

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from functools import wraps

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
        #cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        cur.execute("SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'")
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