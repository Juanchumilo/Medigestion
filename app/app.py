from flask import Flask, render_template, request, redirect,flash,session
from db import get_connection
import models
import bcrypt
import os

app=Flask(__name__)
app.secret_key = os.urandom(24)


#----> Index
@app.route('/')
def index():
    return render_template('index.html')



#----> Ingresar 
@app.route('/ingresar', methods=['GET', 'POST'])
def ingresar():
    if request.method == 'POST':
        correo = request.form['email']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        
        # Buscar si es paciente
        sql = "SELECT * FROM pacientes WHERE email=%s"
        cursor.execute(sql, (correo,))
        usuario = cursor.fetchone()

        if usuario:
            hashed_password = usuario['password']  

            # Verificar contraseña
            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                session['usuario'] = {
                    'id': usuario['id'],
                    'nombre': usuario['nombre'],
                    'apellido': usuario['apellido'],
                    'email': usuario['email']
                }
                cursor.close()
                conn.close()
                return redirect(f"/paciente/{usuario['id']}")
        # Buscar si es medico
        sql = "SELECT * FROM medicos WHERE email=%s"
        cursor.execute(sql, (correo,))
        usuario = cursor.fetchone()

        if usuario:
            hashed_password = usuario['password']  

            # Verificar contraseña
            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                session['usuario'] = {
                    'id': usuario['id'],
                    'nombre': usuario['nombre'],
                    'apellido': usuario['apellido'],
                    'email': usuario['email']
                }
                cursor.close()
                conn.close()
                return redirect(f"/medico/{usuario['id']}")
        
        # Buscar si es admin
        sql = "SELECT * FROM admintb WHERE email=%s"
        cursor.execute(sql, (correo,))
        usuario = cursor.fetchone()
        
        if usuario:
            hashed_password = usuario['password']  

            # Verificar contraseña
            if bcrypt.checkpw(password.encode(), hashed_password.encode()):
                session['usuario'] = {
                    'id': usuario['id'],
                    'nombre': usuario['nombre'],
                    'apellido': usuario['apellido'],
                    'email': usuario['email']
                }
                cursor.close()
                conn.close()
                return redirect(f"/admin/{usuario['id']}")
        # Si no coincide email o contraseña:
        flash("Correo o contraseña incorrectos")
        cursor.close()
        conn.close()

    return render_template('ingresar.html')



#----> Registrarse
@app.route('/registrarse')
def registrarse():
    return render_template('registrarse.html')




#----> Forgot Password
@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword.html')

#Paciente
@app.route('/paciente/<int:id>')
def paciente(id):
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403  

    # Session Exitoso
    return render_template("paciente.html")



#Error 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__=='__main__':
    app.run(debug=True)