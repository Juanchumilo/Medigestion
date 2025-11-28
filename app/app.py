from flask import Flask, render_template, request, redirect,flash,session
from db import get_connection
import models,bcrypt,os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
EMAIL_USER = "medigestioninfo@gmail.com"
EMAIL_PASS = "ouzx atrn tpsr ifwk"


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

        if usuario: #EDITA ESTE ERROR, (IFs)
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
    
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT m.nombre,m.apellido,h.id AS horario_id,h.hora_ingreso,h.hora_ingreso_tp,h.hora_salida,h.hora_salida_tp,h.horario FROM horario_medicos h JOIN medicos m ON h.medico_id = m.id;")
    horarios=cursor.fetchall()
    conn.close()
    cursor.close()


    # Session Exitoso
    return render_template("paciente.html", horarios=horarios)



#Medico
@app.route('/medico/<int:id>')
def medico(id):
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403  

    # Session Exitoso
    return render_template("medico.html")



#Admin
@app.route('/admin/<int:id>')
def admin(id):
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403  

    # Session Exitoso
    return render_template("admin.html")



#-----> Editar Datos-Pacientes
@app.route('/editar_datos/paciente/<int:id>', methods=['GET','POST'])
def editar_datos(id):

    # Verificar sesión
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403

    conn= get_connection()
    cursor = conn.cursor()
    

    if request.method == 'GET':
        cursor.execute("SELECT * FROM pacientes WHERE id=%s", (id,))
        paciente_datos = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template("editar_datos-paciente.html", paciente_datos=paciente_datos)
    
    
    pass1=request.form['password']
    pass2=request.form['confirm_password']
    if request.method=='POST':
        if pass1!=pass2:
            flash('Las contraseñas no coinciden')
            cursor.close()
            conn.close()
            return redirect(f'/editar_datos/paciente/{id}')
            

        data=[request.form['name'],request.form['last_name'],request.form['tipo_documento'],request.form['documento'],request.form['birthdate'],request.form['genero'],request.form['phone'],request.form['email'],request.form['rh'],bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())]

        cursor.execute("UPDATE pacientes SET nombre=%s,apellido=%s,tipo_documento=%s,documento=%s,fecha_nacimiento=%s,genero=%s,telefono=%s,email=%s,rh=%s,password=%s WHERE id=%s",(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],id))
        conn.commit()
        cursor.close()
        conn.close()

        # ACTUALIZAR LA SESIÓN 
        session['usuario']['nombre'] = data[0]
        session['usuario']['apellido'] = data[1]
        session['usuario']['email'] = data[7]

        return redirect(f'/paciente/{id}')



#-----> Editar Datos-Medicos
@app.route('/editar_datos/medico/<int:id>', methods=['GET','POST'])
def editar_datos_medico(id):

    # Verificar sesión
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403

    conn= get_connection()
    cursor = conn.cursor()
    

    if request.method == 'GET':
        cursor.execute("SELECT * FROM medicos WHERE id=%s", (id,))
        medico_datos = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template("editar_datos-medico.html", medico_datos=medico_datos)
    
    
    pass1=request.form['password']
    pass2=request.form['confirm_password']
    if request.method=='POST':
        if pass1!=pass2:
            flash('Las contraseñas no coinciden')
            cursor.close()
            conn.close()
            return redirect(f'editar_datos/medico/{id}')
        
        data=[request.form['name'],request.form['last_name'],request.form['phone'],request.form['email'],bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt()),request.form['documento']]

        cursor.execute("UPDATE medicos SET nombre=%s,apellido=%s,telefono=%s,email=%s,password=%s,documento=%s WHERE id=%s",(data[0],data[1],data[2],data[3],data[4],data[5],id))
        conn.commit()
        cursor.close()
        conn.close()

        # ACTUALIZAR LA SESIÓN 
        session['usuario']['nombre'] = data[0]
        session['usuario']['apellido'] = data[1]
        session['usuario']['email'] = data[3]
        return redirect(f'/medico/{session['usuario']['id']}')



#-----> Editar Datos-Admin
@app.route('/editar_datos/admin/<int:id>', methods=['GET','POST'])
def editar_datos_admin(id):

    # Verificar sesión
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403
    
    conn=get_connection()
    cursor=conn.cursor()


    if request.method == 'GET':
        cursor.execute("SELECT * FROM admintb WHERE id=%s", (id,))
        admin_datos = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template("editar_datos-admin.html", admin_datos=admin_datos)


    pass1=request.form['password']
    pass2=request.form['confirm_password']
    if request.method=='POST':
        if pass1!=pass2:
            flash('Las contraseñas no coinciden')
            cursor.close()
            conn.close()
            return redirect(f'/editar_datos/admin/{id}')
        

        data=[request.form['name'],request.form['last_name'],request.form['email'],bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())]

        cursor.execute("UPDATE admintb SET nombre=%s,apellido=%s,email=%s,password=%s WHERE id=%s",(data[0],data[1],data[2],data[3],id))
        conn.commit()
        conn.close()
        return redirect(f'/admin/{id}')



#------> Ayuda Al Cliente
@app.route('/atencion_cliente',methods=('GET','POST'))
def atencion_cliente():
    if request.method=='POST':
        nombre = request.form['nombre']
        correo = request.form['email']
        motivo = request.form['motivo']
        mensaje = request.form['mensaje']

        # Crear contenido del correo
        asunto = f"Nuevo mensaje de soporte - {motivo}"
        cuerpo = f"""
        Has recibido un nuevo mensaje desde MediGestión:

        Nombre: {nombre}
        Correo: {correo}
        Motivo: {motivo}
        Mensaje:
        {mensaje}
        """

        # Construir correo
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_USER
        msg['Subject'] = asunto
        msg.attach(MIMEText(cuerpo, 'plain'))

        # Enviar correo con SMTP
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string())
            server.quit()

            flash("Mensaje enviado correctamente. Te contactaremos pronto.")
        except Exception as e:
            print("Error enviando correo:", e)
            flash("Hubo un error enviando el mensaje.")

    return render_template('atencion_cliente.html')

    





#--------> Logout
@app.route('/logout')
def logout():
    session.clear()   
    return redirect('/')

#--------> Error 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__=='__main__':
    app.run(debug=True)