from flask import Flask, render_template, request, redirect,flash,session,url_for
from db import get_connection
import models,bcrypt,os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date,datetime
import random
EMAIL_USER = "medigestioninfo@gmail.com"
EMAIL_PASS = "ouzx atrn tpsr ifwk"
#Dia actual
hoy=date.today().isoformat() 




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
                    'email': usuario['email'],
                    'cita_en_proceso':int()
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
@app.route('/paciente/<int:id>', methods=['GET','POST'])
def paciente(id):
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403  
    
    #Horarios Medicos
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT m.nombre,m.apellido,h.id AS horario_id,h.hora_ingreso,h.hora_ingreso_tp,h.hora_salida,h.hora_salida_tp,h.horario FROM horario_medicos h JOIN medicos m ON h.medico_id = m.id;")
    horarios=cursor.fetchall()
    conn.close()
    cursor.close()


    #Ejecutar el Buscar despues del POST
    codigo = request.args.get("codigo")  # viene de la búsqueda
    cita_datos = None
    if codigo:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM citas WHERE id = %s", (codigo,))
        cita_datos = cursor.fetchone()
        cursor.close()
        conn.close()

        return render_template("paciente.html", cita_datos=cita_datos,session=session)
    
    #Form Gestion de Citas
    if request.method == 'POST': 
        accion = request.form["accion"]
        id_codigo = request.form["codigo_cita"]
        conn=get_connection()
        cursor=conn.cursor()

        # ---------- ACCIÓN BUSCAR ----------
        if accion == "buscar":
            if id_codigo:
                return redirect(url_for('paciente', id=id, codigo=id_codigo))
            else:
                flash('Para Buscar una Cita, debe indicar el Código de la Cita')


        # ---------- ACCIÓN CREAR ----------
        if accion == "crear":
            fecha_str = request.form["fecha"]
            hora_str = request.form["hora"]
            motivo = request.form["motivo_cita"]

            if fecha_str and hora_str and motivo:

                if not fecha_str or not hora_str:
                    flash("Fecha y hora obligatorias")
                    return redirect(url_for('paciente', id=id))

                # 2) convertir la fecha y sacar día de la semana (lunes=0 ... domingo=6)
                try:
                    fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
                    dia_semana = fecha_obj.weekday()
                except Exception as e:
                    flash("Formato de fecha inválido")
                    return redirect(url_for('paciente', id=id))

                    
                #Consultar medicos para ese dia en especifico (se elige uno aleatoriamente dentro de los disponibles para ese dia)
                sql_medicos = """
                SELECT m.id, m.nombre, m.apellido
                FROM medicos m
                JOIN horario_dias hd ON hd.medico_id = m.id
                WHERE hd.dia_semana = %s
                """
                cursor.execute(sql_medicos, (dia_semana,))
                medicos = cursor.fetchall()

                if not medicos:
                    flash("No hay médicos que trabajen ese día")
                    cursor.close(); conn.close()
                    return redirect(url_for('paciente', id=id))

                # excluir médicos ya ocupados en ESA fecha y hora 
                sql_ocupados = """
                SELECT medico_id FROM citas
                WHERE fecha = %s AND hora = %s
                """
                cursor.execute(sql_ocupados, (fecha_str, hora_str))
                ocupados_raw = cursor.fetchall()
                ocupados_ids = {r['medico_id'] for r in ocupados_raw}  # set de ids ocupados

                disponibles = [m for m in medicos if m['id'] not in ocupados_ids]

                if not disponibles:
                    flash("Ese día/hora no quedan médicos disponibles")
                    cursor.close()
                    conn.close()
                    return redirect(url_for('paciente', id=id))

                # Elegir aleatoriamente uno entre los medicos disponibles
                medico_elegido = random.choice(disponibles)

                #Crear cita (el consultorio sera establecido de manera aleatoria tambien)
                cursor.execute("INSERT INTO citas (paciente_id, fecha,hora, motivo,consultorio,medico_id) VALUES (%s, %s, %s, %s, %s,%s) ", (id,fecha_str, hora_str, motivo,random.randint(1,3),medico_elegido['id']))
                conn.commit()
                conn.close()
                cursor.close()

                conn=get_connection()
                cursor=conn.cursor()
                cursor.execute("""
                    SELECT * FROM citas 
                    WHERE paciente_id=%s 
                    AND hora=%s 
                    AND motivo=%s 
                    AND medico_id=%s
                """, (id, hora_str, motivo, medico_elegido['id']))

                cita_creada=cursor.fetchall()
                conn.close()
                cursor.close()

                session['cita_en_proceso'] = cita_creada[0]

                return redirect(url_for('efectuarpago', id=id))
            else:
                flash('Necesita completar todos los campos para crear una cita. A excepcion de: Código de Cita')

    return render_template("paciente.html", horarios=horarios, hoy=hoy)



#Medico
@app.route('/medico/<int:id>',methods=['GET','POST'])
def medico(id):
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403  

    # Session Exitoso

    #Horario Actual
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM horario_medicos WHERE medico_id=%s",(id))
    horario=cursor.fetchone()
    conn.close()
    cursor.close()

    if request.method=='POST':
        hora_ingreso=request.form['hora_ingreso']
        hora_ingreso_tp=request.form['hora_ingreso_tp']
        hora_salida=request.form['hora_salida']
        hora_salida_tp=request.form['hora_salida_tp']
        horario=request.form['horario']

        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE horario_medicos SET hora_ingreso=%s,hora_ingreso_tp=%s,hora_salida=%s,hora_salida_tp=%s,horario=%s WHERE medico_id=%s",(hora_ingreso,hora_ingreso_tp,hora_salida,hora_salida_tp,horario,id))
        conn.commit()

        conn.close()
        cursor.close()

        flash('Horario Actualizado Correctamente')
        return redirect(url_for('medico',id=id))
    
    #Gestionar Reportes

    sql = """
    SELECT c.id, c.fecha, c.hora, c.motivo, c.estado, c.consultorio,
        p.id AS paciente_id, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
        m.id AS medico_id, m.nombre AS medico_nombre, m.apellido AS medico_apellido
    FROM citas c
    JOIN pacientes p ON c.paciente_id = p.id
    JOIN medicos m ON c.medico_id = m.id
    WHERE c.medico_id = %s 
    """


    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(sql, (id))  
    cita_detalles = cursor.fetchall()   
    cursor.close()
    conn.close()


    return render_template("medico.html",horario=horario,cita_detalles=cita_detalles)



#Admin
@app.route('/admin/<int:id>', methods=['GET','POST'])
def admin(id):
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403  

    # Session Exitoso

    #Horarios Medicos
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute("SELECT m.nombre,m.apellido,h.id AS horario_id,h.hora_ingreso,h.hora_ingreso_tp,h.hora_salida,h.hora_salida_tp,h.horario FROM horario_medicos h JOIN medicos m ON h.medico_id = m.id;")
    horarios=cursor.fetchall()
    conn.close()
    cursor.close()

    
    
    return render_template("admin.html", horarios=horarios)



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

    

#Editar cita medica --> PACIENTE
@app.route('/paciente/editar_cita/<int:id>', methods=('GET','POST'))
def editar_cita_paciente(id):
    # Verificar sesión
    if 'usuario' not in session:
        return redirect('/ingresar')
    
    conn= get_connection()
    cursor= conn.cursor()
    cursor.execute('SELECT * FROM citas WHERE id=%s',(id))
    datos_cita=cursor.fetchone()
    conn.close()
    cursor.close()



    if request.method == 'POST':
        fecha= (request.form['fecha'].replace("/", "-"))
        hora = request.form['hora']
        motivo = request.form['motivo']
        estado = request.form['estado']
        



        # Si la cita sigue programada → actualizar
        if estado == 'Programada':
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE citas SET fecha=%s, hora=%s, motivo=%s WHERE id=%s',(fecha, hora, motivo, id))
            conn.commit()
            cursor.close()
            conn.close()

        # Si la cita fue cancelada → eliminar
        elif estado == 'Cancelada':
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM citas WHERE id=%s",(id))
            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('paciente', id=session['usuario']['id']))
    return render_template('editar_cita_paciente.html',datos_cita=datos_cita, hoy=hoy)



#-------> Efectuar Pago-Paciente
@app.route('/paciente/pago/<int:id>', methods=['GET','POST'])
def efectuarpago(id):
    # Verificar sesión
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403
    
    cita = session['cita_en_proceso']['id']
    
    if request.method=='POST':
        cita = session['cita_en_proceso']['id']
        email=request.form['email']
        metodo_pago=request.form['metodo-pago']
        conn=get_connection()
        cursor=conn.cursor()
        
        cursor.execute("INSERT INTO efectuar_pago (email,metodo_pago,paciente,cita_pagada) VALUES (%s,%s,%s,%s)",(email,metodo_pago,id,cita))
        conn.commit()
        conn.close()
        cursor.close()

        flash('Pago y Cita hechos correctamente')
        flash(f'El codigo de su Cita creada es: {cita}')
        return redirect(url_for('paciente', id=id))
    
    return render_template('realizar_pago.html', cita=cita)



#-------> Generar Reportes-Medico
@app.route('/medico/reporte/<int:id>', methods=['GET','POST'])
def medico_reporte(id):
    if 'usuario' not in session:
        return redirect('/ingresar')
    
    conn=get_connection()
    cursor=conn.cursor()
    sql = """
    SELECT c.id, c.fecha, c.hora, c.motivo, c.estado, c.consultorio, c.observaciones,
        p.id AS paciente_id, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
        m.id AS medico_id, m.nombre AS medico_nombre, m.apellido AS medico_apellido
    FROM citas c
    JOIN pacientes p ON c.paciente_id = p.id
    JOIN medicos m ON c.medico_id = m.id
    WHERE c.id = %s 
    """
    cursor.execute(sql,id)
    cita=cursor.fetchone()
    conn.close()
    cursor.close()


    if request.method=='POST':
        motivo=request.form['motivo-cita']
        observaciones=request.form['observaciones']
        estado='Completada'

        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE citas SET motivo=%s,observaciones=%s,estado=%s WHERE id=%s",(motivo,observaciones,estado,id))
        conn.commit()
        conn.close()
        cursor.close()


        flash('Reporte generado con exito')
        return redirect(url_for('medico',id=cita['medico_id']))



    return render_template('reportes.html', cita=cita)



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