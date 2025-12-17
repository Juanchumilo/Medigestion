from flask import Flask, render_template, request, redirect,flash,session,url_for
from db import get_connection
import models,bcrypt,os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date,datetime
import random
import funciones_adicionales as fun_ad
EMAIL_USER = "medigestioninfo@gmail.com"
EMAIL_PASS = "ouzx atrn tpsr ifwk"
#Dia actual
hoy=date.today().isoformat() 




app=Flask(__name__)
app.secret_key = os.urandom(24)

########################################################    PAGINAS AUTH    ########################################################

#----> Index 
@app.route('/')
def index():
    return render_template('auth/index.html')



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

    return render_template('auth/ingresar.html')



#----> Registrarse
@app.route('/registrarse', methods=['GET','POST'])
def registrarse():
    if request.method=='POST':
        if request.form['password']==request.form['confirm_password']:
            nombre=request.form['name'].strip().upper()
            apellido=request.form['last_name'].strip().upper()
            email=request.form['email']
            fecha_nacimiento=request.form['birthdate']
            telefono=request.form['phone']
            tipo_documento=request.form['tipo-documento']
            documento=request.form['documento']
            rh=request.form['rh']
            genero=request.form['genero']
            password=bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())

            conn=get_connection()
            cursor=conn.cursor()
            try:
                cursor.execute('INSERT INTO pacientes (nombre,apellido,email,fecha_nacimiento,telefono,tipo_documento,documento,rh,genero,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(nombre,apellido,email,fecha_nacimiento,telefono,tipo_documento,documento,rh,genero,password))
                conn.commit()

            except pymysql.err.IntegrityError as e:
                error_msg = str(e)

                if "pacientes.telefono" in error_msg:
                    flash("El teléfono ingresado ya está registrado.", "error")

                elif "pacientes.email" in error_msg:
                    flash("El correo ingresado ya está registrado.", "error")

                elif "pacientes.documento" in error_msg:
                    flash("El documento ingresado ya está registrado.", "error")

                else:
                    flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

                return redirect(url_for("registrarse"))

            finally:
                cursor.close()
                conn.close()
            flash('Usuario registrado correctamente')
            return redirect(url_for('ingresar'))
        else:
            flash('Las contraseñas no coinciden')
    return render_template('auth/registrarse.html')



#----> Forgot Password 
@app.route('/forgotpassword')
def forgotpassword():
    return render_template('auth/forgotpassword.html')



#--------> Logout
@app.route('/logout')
def logout():
    session.clear()   
    return redirect('/')


########################################################    PAGINAS USUARIOS   ########################################################

#Paciente ===================================================================>
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
        if session['usuario']['id']==cita_datos['paciente_id']:
            cursor.close()
            conn.close()
        
            return render_template("paciente/paciente.html", cita_datos=cita_datos,session=session)
        else:
            flash('No tiene una cita registrada a su nombre con ese Código','cita')

    
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
                flash('Para Buscar una Cita, debe indicar el Código de la Cita','cita')


        # ---------- ACCIÓN CREAR ----------
        if accion == "crear":
            cursor=get_connection().cursor()
            fecha_str = request.form["fecha"]
            cursor.execute('SELECT COUNT(*) FROM citas WHERE fecha=%s',(fecha_str))
            citas_diarias= cursor.fetchall()[0]
            cursor.close()

            if len(citas_diarias) < len(fun_ad.config()):
                hora_str = request.form["hora"]
                motivo = request.form["motivo_cita"].capitalize

                if fecha_str and hora_str and motivo:

                    if not fecha_str or not hora_str:
                        flash("Fecha y hora obligatorias",'cita')
                        return redirect(url_for('paciente', id=id))

                    # 2) convertir la fecha y sacar día de la semana (lunes=0 ... domingo=6)
                    try:
                        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
                        dia_semana = fecha_obj.weekday()
                    except Exception as e:
                        flash("Formato de fecha inválido",'cita')
                        return redirect(url_for('paciente', id=id))

                        
                    #Consultar medicos para ese dia en especifico (se elige uno aleatoriamente dentro de los disponibles para ese dia)
                    sql_medicos = """
                    SELECT m.id, m.nombre, m.apellido
                    FROM medicos m
                    JOIN horario_dias hd ON hd.medico_id = m.id
                    WHERE hd.dia_semana = %s
                    """
                    conn=get_connection()
                    cursor=conn.cursor()
                    cursor.execute(sql_medicos, (dia_semana,))
                    medicos = cursor.fetchall()
                    cursor.close(); conn.close()

                    if not medicos:
                        flash("No hay médicos que trabajen ese día",'cita')
                        return redirect(url_for('paciente', id=id))

                    # excluir médicos ya ocupados en ESA fecha y hora 
                    sql_ocupados = """
                    SELECT medico_id FROM citas
                    WHERE fecha = %s AND hora = %s
                    """
                    conn=get_connection()
                    cursor=conn.cursor()
                    cursor.execute(sql_ocupados, (fecha_str, hora_str))
                    ocupados_raw = cursor.fetchall()
                    cursor.close(); conn.close()
                    ocupados_ids = {r['medico_id'] for r in ocupados_raw}  # set de ids ocupados

                    disponibles = [m for m in medicos if m['id'] not in ocupados_ids]

                    if not disponibles:
                        flash("Ese día/hora no quedan médicos disponibles",'cita')
                        return redirect(url_for('paciente', id=id))

                    # Elegir aleatoriamente uno entre los medicos disponibles
                    medico_elegido = random.choice(disponibles)

                    #Crear cita (el consultorio sera establecido de manera aleatoria tambien)
                    conn=get_connection()
                    cursor=conn.cursor()
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

                    session['cita_en_proceso']=cursor.fetchone()
                    conn.close()
                    cursor.close()

                    return redirect(url_for('efectuarpago', id=id))
                else:
                    flash('Necesita completar todos los campos para crear una cita. A excepcion de: Código de Cita','cita')
            else:
                flash('Se alcanzó el número máximo de citas diarias, Por favor escoga otra fecha para la cita','cita')
                return redirect(url_for('paciente', id=session['usuario']['id']))

    return render_template("paciente/paciente.html", horarios=horarios, hoy=hoy)



#Medico ==========================================================================>
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


    return render_template("medico/medico.html",horario=horario,cita_detalles=cita_detalles)



#Admin ================================================================================>
@app.route('/admin/<int:id>', methods=['GET','POST'])
def admin(id):

    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403  

    # ===== PAGINACIÓN =====
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = 5
    offset = (pagina - 1) * por_pagina

    # ------ Horarios Médicos ------
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.nombre, m.apellido, h.id AS horario_id, h.hora_ingreso, 
        h.hora_ingreso_tp, h.hora_salida, h.hora_salida_tp, h.horario 
        FROM horario_medicos h 
        JOIN medicos m ON h.medico_id = m.id;
    """)
    horarios = cursor.fetchall()
    conn.close()
    cursor.close()

    # ------ Pacientes con paginación ------
    conn = get_connection()
    cursor = conn.cursor()

    # Contar total
    cursor.execute("SELECT COUNT(*) AS total FROM pacientes")
    total_pacientes = cursor.fetchone()['total']

    # Página actual
    cursor.execute("""
        SELECT id,nombre, apellido, email
        FROM pacientes
        LIMIT %s OFFSET %s
    """, (por_pagina, offset))
    pacientes = cursor.fetchall()

    conn.close()
    cursor.close()

    hay_mas = pagina * por_pagina < total_pacientes

    # ------ Médicos ------

    # ===== MEDICOS PAGINACIÓN =====
    pagina_medicos = request.args.get('pagina_medicos', 1, type=int)
    por_pagina = 5
    offset = (pagina_medicos - 1) * por_pagina
    # ------ Medicos con paginación ------
    conn = get_connection()
    cursor = conn.cursor()

    # Contar total
    cursor.execute("SELECT COUNT(*) AS total FROM medicos")
    total_medicos = cursor.fetchone()['total']

    # Página actual
    cursor.execute("""
        SELECT id,nombre, apellido, email
        FROM medicos
        LIMIT %s OFFSET %s
    """, (por_pagina, offset))
    medicos = cursor.fetchall()

    conn.close()
    cursor.close()

    hay_mas_medicos = pagina_medicos * por_pagina < total_medicos


    #-------Gestionar citas---------

    # ===== SEGUNDA PAGINACIÓN =====
    paginacita = request.args.get('paginacita', 1, type=int)
    por_pagina_2 = 5
    offset_citas = (paginacita - 1) * por_pagina_2

    # ------ Citas con paginación ------
    conn = get_connection()
    cursor = conn.cursor()

    # Contar total
    cursor.execute("SELECT COUNT(*) AS total FROM citas")
    total_citas = cursor.fetchone()['total']

    # Página actual
    cursor.execute("""
        SELECT c.id, c.fecha, c.hora, c.motivo, c.estado, c.consultorio,c.estado,
        p.id AS paciente_id, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido,
        m.id AS medico_id, m.nombre AS medico_nombre, m.apellido AS medico_apellido
    FROM citas c
    JOIN pacientes p ON c.paciente_id = p.id
    JOIN medicos m ON c.medico_id = m.id 
        LIMIT %s OFFSET %s
    """, (por_pagina_2, offset_citas))
    citas = cursor.fetchall()

    conn.close()
    cursor.close()

    hay_mas_citas = paginacita * por_pagina_2 < total_citas

    #======= Valores Predeterminados Gestion del Sitema ========#
    config = fun_ad.config()

    #======= UPDATE de valores de Gestion del Sitema ========#
    if request.method=='POST':
        max_usuarios=request.form['max_usuarios']
        max_citas_diarias=request.form['max_citas_diarias']
        notificaciones=request.form['notificaciones']

        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute('UPDATE configuracion_sistema SET max_usuarios=%s,max_citas_diarias=%s,notificaciones=%s WHERE id=%s',(max_usuarios,max_citas_diarias,notificaciones,1))
        conn.commit()
        conn.close()
        cursor.close()

        flash('Sistema Editado correctamente','sistema')
        return redirect(url_for('admin',id=session['usuario']['id']))

    return render_template("""admin/admin.html""",
    horarios=horarios,
    pacientes=pacientes,
    medicos=medicos,
    pagina=pagina,
    pagina_medicos=pagina_medicos,
    hay_mas=hay_mas,
    hay_mas_medicos=hay_mas_medicos, 
    citas=citas,
    paginacita=paginacita,
    hay_mas_citas=hay_mas_citas,
    config=config)




########################################################    PAGINAS COMPLEMENTARIAS   ########################################################


################===PACIENTE===################
#-----> Editar Datos-Pacientes <----------#
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

        return render_template("paciente/editar_datos-paciente.html", paciente_datos=paciente_datos,hoy=hoy)
    
    if request.method=='POST':
        if request.form['password']!=request.form['confirm_password']:
            flash('Las contraseñas no coinciden','datos')
            cursor.close()
            conn.close()
            return redirect(f'/editar_datos/paciente/{id}')
            

        #Editar Datos
        data=[request.form['nombre'].strip().upper(),request.form['apellido'].strip().upper(),request.form['tipo_documento'],request.form['documento'],request.form['birthdate'],request.form['genero'],request.form['phone'],request.form['email'],request.form['rh'],bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())]
        try:
            cursor.execute("UPDATE pacientes SET nombre=%s,apellido=%s,tipo_documento=%s,documento=%s,fecha_nacimiento=%s,genero=%s,telefono=%s,email=%s,rh=%s,password=%s WHERE id=%s",(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],id))
            conn.commit()

        except pymysql.err.IntegrityError as e:
            error_msg = str(e)

            if "pacientes.telefono" in error_msg:
                flash("El teléfono ingresado ya está registrado.", "error")

            elif "pacientes.email" in error_msg:
                flash("El correo ingresado ya está registrado.", "error")

            elif "pacientes.documento" in error_msg:
                flash("El documento ingresado ya está registrado.", "error")

            else:
                flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

                return redirect(url_for("paciente",id=id))

        finally:
            cursor.close()
            conn.close()
        cursor.execute("UPDATE pacientes SET nombre=%s,apellido=%s,tipo_documento=%s,documento=%s,fecha_nacimiento=%s,genero=%s,telefono=%s,email=%s,rh=%s,password=%s WHERE id=%s",(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],id))
        conn.commit()
        cursor.close()
        conn.close()

        # ACTUALIZAR LA SESIÓN 
        session['usuario']['nombre'] = data[0]
        session['usuario']['apellido'] = data[1]
        session['usuario']['email'] = data[7]

        flash('Datos del Usuario editados con éxito')
        return redirect(f'/paciente/{id}')

#---------> Editar cita medica-Paciente <----------#
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
        motivo = request.form['motivo'].capitalize
        accion=request.form['accion']
        


        # 2) convertir la fecha y sacar día de la semana (lunes=0 ... domingo=6)
        try:
            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
            dia_semana = fecha_obj.weekday()
        except Exception as e:
            flash("Formato de fecha inválido",'error')
            return redirect(url_for('editar_cita_paciente', id=session['usuario']['id']))


        # Si la cita sigue programada → actualizar
        if accion == 'editar':
            conn = get_connection()
            cursor = conn.cursor()

            sql_medicos = """
                    SELECT m.id, m.nombre, m.apellido
                    FROM medicos m
                    JOIN horario_dias hd ON hd.medico_id = m.id
                    WHERE hd.dia_semana = %s
                    """
            cursor.execute(sql_medicos, (dia_semana,))
            medicos = cursor.fetchall()
            cursor.close(); conn.close()

            if not medicos:
                flash("No hay médicos que trabajen ese día",'error')
                return redirect(url_for('editar_cita_paciente', id=session['usuario']['id']))

            # excluir médicos ya ocupados en ESA fecha y hora 
            sql_ocupados = """
            SELECT medico_id FROM citas
            WHERE fecha = %s AND hora = %s
            """
            conn=get_connection()
            cursor=conn.cursor()
            cursor.execute(sql_ocupados, (fecha_str, hora_str))
            ocupados_raw = cursor.fetchall()
            cursor.close(); conn.close()
            ocupados_ids = {r['medico_id'] for r in ocupados_raw}  # set de ids ocupados

            disponibles = [m for m in medicos if m['id'] not in ocupados_ids]

            if not disponibles:
                flash("Ese día/hora no quedan médicos disponibles",'error')
                return redirect(url_for('editar_cita_paciente', id=session['usuario']['id']))



            # Editar datos de la cita (solo despues de las anteriores confirmaciones)
            try:
                cursor.execute('UPDATE citas SET fecha=%s, hora=%s, motivo=%s WHERE id=%s',(fecha, hora, motivo, id))
                conn.commit()

            except pymysql.err.IntegrityError as e:
                flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

                return redirect(url_for("paciente",id=session['usuario']['id']))

            finally:
                cursor.close()
                conn.close()

        # Si la cita fue cancelada → eliminar
        elif accion == 'eliminar':
            conn = get_connection()
            cursor = conn.cursor()

            try:
                # 1. Eliminar pagos relacionados con la cita
                cursor.execute("DELETE FROM efectuar_pago WHERE cita_pagada = %s", (id,))

                # 2. Eliminar la cita
                cursor.execute("DELETE FROM citas WHERE id = %s", (id,))

                conn.commit()

            except Exception as e:
                conn.rollback()
                flash("Error al eliminar la cita: " + str(e))

            finally:
                cursor.close()
                conn.close()

            flash('Cita eliminada correctamente','cita')
            return redirect(url_for('paciente', id=session['usuario']['id']))
    return render_template('paciente/editar_cita_paciente.html',datos_cita=datos_cita, hoy=hoy)

#-------> Efectuar Pago-Paciente <----------#
@app.route('/paciente/pago/<int:id>', methods=['GET','POST'])
def efectuarpago(id):
    # Verificar sesión
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403
    
    cita = session['cita_en_proceso']
    
    if request.method=='POST':
        cita = session['cita_en_proceso']
        email=request.form['email']
        metodo_pago=request.form['metodo-pago']
        conn=get_connection()
        cursor=conn.cursor()
        
        cursor.execute("INSERT INTO efectuar_pago (email,metodo_pago,paciente,cita_pagada) VALUES (%s,%s,%s,%s)",(email,metodo_pago,id,cita['id']))
        conn.commit()
        conn.close()
        cursor.close()

        flash('Pago y Cita hechos correctamente','cita')
        flash(f'El codigo de su Cita creada es: {cita['id']}','cita')
        return redirect(url_for('paciente', id=id))
    
    return render_template('otros/realizar_pago.html', cita=cita)




################===MEDICO===################
#-----> Editar Datos-Medicos <----------#
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

        return render_template("medico/editar_datos-medico.html", medico_datos=medico_datos)
    
    if request.method=='POST':
        if request.form['password']!=request.form['confirm_password']:
            flash('Las contraseñas no coinciden','datos')
            cursor.close()
            conn.close()
            return redirect(f'editar_datos/medico/{id}')
        
        data=[request.form['name'].strip().upper(),request.form['last_name'].strip().upper(),request.form['phone'],request.form['email'],bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt()),request.form['documento']]


        try:
            cursor.execute("UPDATE medicos SET nombre=%s,apellido=%s,telefono=%s,email=%s,password=%s,documento=%s WHERE id=%s",(data[0],data[1],data[2],data[3],data[4],data[5],id))
            conn.commit()

        except pymysql.err.IntegrityError as e:
            error_msg = str(e)

            if "medicos.telefono" in error_msg:
                flash("El teléfono ingresado ya está registrado.", "error")

            elif "medicos.email" in error_msg:
                flash("El correo ingresado ya está registrado.", "error")

            elif "medicos.documento" in error_msg:
                flash("El documento ingresado ya está registrado.", "error")

            else:
                flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

            return redirect(url_for("editar_datos_medico",id=id))

        finally:
            cursor.close()
            conn.close()


        # ACTUALIZAR LA SESIÓN 
        session['usuario']['nombre'] = data[0]
        session['usuario']['apellido'] = data[1]
        session['usuario']['email'] = data[3]

        flash('Datos del Usuario editados con éxito','editar_datos')
        return redirect(f'/medico/{session['usuario']['id']}')

#-------> Generar Reportes-Medico <----------#
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
        motivo=request.form['motivo-cita'].capitalize
        observaciones=request.form['observaciones']
        estado='Completada'

        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE citas SET motivo=%s,observaciones=%s,estado=%s WHERE id=%s",(motivo,observaciones,estado,id))
        conn.commit()
        conn.close()
        cursor.close()


        flash('Reporte generado con exito','reporte')
        return redirect(url_for('medico',id=cita['medico_id']))

    return render_template('medico/reportes.html', cita=cita)




################===ADMIN===################
#-----> Editar Datos-Admin <----------#
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

        return render_template("admin/editar_datos-admin.html", admin_datos=admin_datos)

    if request.method=='POST':
        if request.form['password']!=request.form['confirm_password']:
            flash('Las contraseñas no coinciden','datos')
            cursor.close()
            conn.close()
            return redirect(f'/editar_datos/admin/{id}')
        

        data=[request.form['name'].strip().upper(),request.form['last_name'].strip().upper(),request.form['email'],bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())]

        try:
            cursor.execute("UPDATE admintb SET nombre=%s,apellido=%s,email=%s,password=%s WHERE id=%s",(data[0],data[1],data[2],data[3],id))
            conn.commit()

        except pymysql.err.IntegrityError as e:
            error_msg = str(e)

            if "admintb.email" in error_msg:
                flash("El correo ingresado ya está registrado.", "error")

            else:
                flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

            return redirect(url_for("editar_datos_admin",id=id))

        finally:
            cursor.close()
            conn.close()

        flash('Datos del Usuario editados con éxito','editar_datos')
        return redirect(f'/admin/{id}')

#-------> Gestion de Usuarios_paciente-Admin <----------#
@app.route('/admin/gestion-usuarios/paciente/<int:id>', methods=['GET','POST'])
def gestion_usuarios_paciente(id):
    if 'usuario' not in session:
        return redirect('/ingresar')
    
    #===== Valores Predeterminados ======
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE id=%s',(id))
    datos=cursor.fetchone()
    conn.close()
    cursor.close()

    if request.method=='POST':
        if request.form['password'] == request.form['confirm_password']:
            nombre=request.form['nombre'].strip().upper()
            apellido=request.form['apellido'].strip().upper()
            tipo_documento=request.form['tipo_documento']
            documento=request.form['documento']
            birthdate=request.form['birthdate']
            genero=request.form['genero']
            telefono=request.form['telefono']
            email=request.form['email']
            rh=request.form['rh']
            password=bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())

            sql='UPDATE pacientes SET nombre=%s,apellido=%s,tipo_documento=%s,documento=%s,fecha_nacimiento=%s,genero=%s,telefono=%s,email=%s,rh=%s,password=%s WHERE id=%s'

            conn=get_connection()
            cursor=conn.cursor()

            try:
                cursor.execute(sql,(nombre,apellido,tipo_documento,documento,birthdate,genero,telefono,email,rh,password,id))
                conn.commit()

            except pymysql.err.IntegrityError as e:
                error_msg = str(e)

                if "pacientes.telefono" in error_msg:
                    flash("El teléfono ingresado ya está registrado.", "error")

                elif "pacientes.email" in error_msg:
                    flash("El correo ingresado ya está registrado.", "error")

                elif "pacientes.documento" in error_msg:
                    flash("El documento ingresado ya está registrado.", "error")

                else:
                    flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

                return redirect(url_for("gestion_usuarios_paciente", id=id))

            finally:
                cursor.close()
                conn.close()

            flash('Usuario Editado con éxito','usuario')
            return redirect(url_for('admin', id=session['usuario']['id']))
        
        else:
            flash('Las contraseñas ingresadas no coinciden')
            return redirect(url_for('gestion_usuario_paciente',id=id))


    return render_template('admin/gestion_usuarios_paciente.html',datos=datos,hoy=hoy)

#-------> Gestion de Usuarios_medico-Admin <----------#
@app.route('/admin/gestion-usuarios/medico/<int:id>', methods=['GET','POST'])
def gestion_usuarios_medico(id):
    if 'usuario' not in session:
        return redirect('/ingresar')
    
    #===== Valores Predeterminados ======
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM medicos WHERE id=%s',(id))
    datos=cursor.fetchone()
    conn.close()
    cursor.close()

    if request.method=='POST':
        if request.form['password'] == request.form['confirm_password']:
            nombre=request.form['nombre'].strip().upper()
            apellido=request.form['apellido'].strip().upper()
            documento=request.form['documento']
            telefono=request.form['telefono']
            email=request.form['email']
            password=bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())

            sql='UPDATE medicos SET nombre=%s,apellido=%s,documento=%s,telefono=%s,email=%s,password=%s WHERE id=%s'

            conn=get_connection()
            cursor=conn.cursor()

            try:
                cursor.execute(sql,(nombre,apellido,documento,telefono,email,password,id))
                conn.commit()

            except pymysql.err.IntegrityError as e:
                error_msg = str(e)

                if "medicos.telefono" in error_msg:
                    flash("El teléfono ingresado ya está registrado.", "error")

                elif "medicos.email" in error_msg:
                    flash("El correo ingresado ya está registrado.", "error")

                elif "medicos.documento" in error_msg:
                    flash("El documento ingresado ya está registrado.", "error")

                else:
                    flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

                return redirect(url_for("gestion_usuarios_medico",id=id))

            finally:
                cursor.close()
                conn.close()

            flash('Usuario Editado con éxito','usuario')
            return redirect(url_for('admin', id=session['usuario']['id']))
        
        else:
            flash('Las contraseñas ingresadas no coinciden')
            return redirect(url_for('gestion_usuario_paciente',id=id))


    return render_template('admin/gestion_usuarios_medico.html',datos=datos,hoy=hoy)

#-------> Gestion de Citas-Admin <----------#
@app.route('/admin/gestionar-cita/<int:id>', methods=['GET','POST'])
def gestionar_cita(id):
    if 'usuario' not in session:
        return redirect('/ingresar')
    

    #====== Valores predefinidos ======#
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

    cursor.execute(sql,(id))
    datos_cita=cursor.fetchone()
    conn.close()
    cursor.close()

    #====== Lista de Pacientes ======#
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT pacientes.nombre,pacientes.apellido,pacientes.id FROM pacientes')
    pacientes=cursor.fetchall()
    conn.close()
    cursor.close()

    #====== Lista de Medicos ======#
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT medicos.nombre,medicos.apellido,medicos.id FROM medicos')
    medicos=cursor.fetchall()
    conn.close()
    cursor.close()

    #====== Lista de Consultorios ======#
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT consultorio.nombre,consultorio.id FROM consultorio')
    consultorios=cursor.fetchall()
    conn.close()
    cursor.close()

    if request.method=='POST':
        accion = request.form["accion"]
        if accion == 'editar':
            paciente_seleccionado=request.form['paciente_seleccionado']
            medico_seleccionado=request.form['medico_seleccionado']
            consultorio_seleccionado=request.form['consultorio_seleccionado']
            fecha=(request.form['fecha'].replace("/", "-"))
            hora=request.form['hora']
            motivo=request.form['motivo'].capitalize
            observaciones=request.form['observaciones']

            # 2) convertir la fecha y sacar día de la semana (lunes=0 ... domingo=6)
            try:
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                dia_semana = fecha_obj.weekday()
            except Exception as e:
                flash("Formato de fecha inválido",'error')
                return redirect(url_for('gestionar_cita', id=id))

            conn = get_connection()
            cursor = conn.cursor()

            sql_medicos = """
                    SELECT m.id, m.nombre, m.apellido
                    FROM medicos m
                    JOIN horario_dias hd ON hd.medico_id = m.id
                    WHERE hd.dia_semana = %s
                    """
            cursor.execute(sql_medicos, (dia_semana,))
            medicos = cursor.fetchall()
            cursor.close(); conn.close()

            if not medicos:
                flash("No hay médicos que trabajen ese día",'error')
                return redirect(url_for('gestionar_cita', id=id))

            # excluir médicos ya ocupados en ESA fecha y hora 
            sql_ocupados = """
            SELECT medico_id FROM citas
            WHERE fecha = %s AND hora = %s
            """
            conn=get_connection()
            cursor=conn.cursor()
            cursor.execute(sql_ocupados, (fecha_str, hora_str))
            ocupados_raw = cursor.fetchall()
            cursor.close(); conn.close()
            ocupados_ids = {r['medico_id'] for r in ocupados_raw}  # set de ids ocupados

            disponibles = [m for m in medicos if m['id'] not in ocupados_ids]

            if not disponibles:
                flash("Ese día/hora no quedan médicos disponibles",'error')
                return redirect(url_for('gestionar_cita', id=id))
            

            # Editar datos de la cita (solo despues de las anteriores confirmaciones)
            try:
                sql='UPDATE citas SET paciente_id=%s,medico_id=%s,consultorio=%s,motivo=%s,fecha=%s,hora=%s,observaciones=%s WHERE id=%s'
                cursor.execute(sql,(paciente_seleccionado,medico_seleccionado,consultorio_seleccionado,motivo,fecha,hora,observaciones,id))
                conn.commit()

            except pymysql.err.IntegrityError as e:

                flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")
                return redirect(url_for("gestionar_cita",id=id))

            finally:
                cursor.close()
                conn.close()

            flash('Cita Editada Correctamente')
            return redirect(url_for('admin', id=session['usuario']['id']))
        elif accion=='eliminar':
            conn = get_connection()
            cursor = conn.cursor()

            try:
                # 1. Eliminar pagos relacionados con la cita
                cursor.execute("DELETE FROM efectuar_pago WHERE cita_pagada = %s", (id,))

                # 2. Eliminar la cita
                cursor.execute("DELETE FROM citas WHERE id = %s", (id,))

                conn.commit()
                flash("Cita eliminada correctamente")

            except Exception as e:
                conn.rollback()
                flash("Error al eliminar la cita: " + str(e))

            finally:
                cursor.close()
                conn.close()

            return redirect(url_for('admin', id=session['usuario']['id']))

    return render_template('admin/gestionar_cita.html',datos_cita=datos_cita,pacientes=pacientes,medicos=medicos,consultorios=consultorios)

#-------> Creacion de Usuarios-Admin <----------#
@app.route('/admin/crear-usuario/<int:id>',methods=['GET','POST'])
def crear_usuario(id):
    # Verificar sesión
    if 'usuario' not in session:
        return redirect('/ingresar')

    if session['usuario']['id'] != id:
        return "Acceso no autorizado", 403


    tipo_usuario = request.args.get('tipo_usuario')

    if request.method == 'POST':
        accion = request.form.get('accion')

        if accion == 'eleccion' and not tipo_usuario:
            tipo_usuario = request.form.get('tipo_usuario')
            return redirect(url_for('crear_usuario',id=session['usuario']['id'],tipo_usuario=tipo_usuario))

        else:
            if tipo_usuario=='pacientes':
                if request.form['usuario']=='crear_paciente':
                    if request.form['p_password']==request.form['p_confirm_password']:
                        nombre=request.form['p_nombre'].strip().upper()
                        apellido=request.form['p_apellido'].strip().upper()
                        email=request.form['p_email']
                        password= bcrypt.hashpw(request.form['p_password'].encode(), bcrypt.gensalt())
                        fecha_nacimiento=request.form['p_birthdate']
                        telefono=request.form['p_telefono']
                        tipo_documento=request.form['p_tipo_documento']
                        documento=request.form['p_documento']
                        rh=request.form['p_rh']
                        genero=request.form['p_genero']

                        conn=get_connection()
                        cursor=conn.cursor()
                        sql='INSERT INTO pacientes (nombre,apellido,email,password,fecha_nacimiento,telefono,tipo_documento,documento,rh,genero) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'


                        try:
                            cursor.execute(sql,(nombre,apellido,email,password,fecha_nacimiento,telefono,tipo_documento,documento,rh,genero))
                            conn.commit()

                        except pymysql.err.IntegrityError as e:
                            error_msg = str(e)

                            if "pacientes.telefono" in error_msg:
                                flash("El teléfono ingresado ya está registrado.", "error")

                            elif "pacientes.email" in error_msg:
                                flash("El correo ingresado ya está registrado.", "error")

                            elif "pacientes.documento" in error_msg:
                                flash("El documento ingresado ya está registrado.", "error")

                            else:
                                flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

                            return redirect(url_for("crear_usuario",id=session['usuario']['id']))

                        finally:
                            conn.close()
                            cursor.close()

                        flash('Usuario - Paciente creado exitosamente','usuario')
                        return redirect(url_for('admin',id=session['usuario']['id']))

            elif tipo_usuario=='medicos':
                if request.form['usuario']=='crear_medico':
                    if request.form['m_password']==request.form['m_confirm_password']:
                        nombre=request.form['m_nombre'].strip().upper()
                        apellido=request.form['m_apellido'].strip().upper()
                        email=request.form['m_email']
                        password= bcrypt.hashpw(request.form['m_password'].encode(), bcrypt.gensalt())
                        telefono=request.form['m_telefono']
                        documento=request.form['m_documento']

                        conn=get_connection()
                        cursor=conn.cursor()

                        sql='INSERT INTO medicos (nombre,apellido,email,password,telefono,documento) VALUES (%s,%s,%s,%s,%s,%s)'

                        try:
                            cursor.execute(sql,(nombre,apellido,email,password,telefono,documento))
                            conn.commit()

                        except pymysql.err.IntegrityError as e:
                            error_msg = str(e)

                            if "medicos.telefono" in error_msg:
                                flash("El teléfono ingresado ya está registrado.", "error")

                            elif "medicos.email" in error_msg:
                                flash("El correo ingresado ya está registrado.", "error")

                            elif "medicos.documento" in error_msg:
                                flash("El documento ingresado ya está registrado.", "error")

                            else:
                                flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

                            return redirect(url_for("crear_usuario",id=session['usuario']['id']))

                        finally:
                            conn.close()
                            cursor.close()

                        flash('Usuario - Medico creado exitosamente','usuario')
                        return redirect(url_for('admin',id=session['usuario']['id']))

            elif tipo_usuario=='admintb':
                if request.form['usuario']=='crear_admin':
                    if request.form['a_password']==request.form['a_confirm_password']:
                        nombre=request.form['a_nombre'].strip().upper()
                        apellido=request.form['a_apellido'].strip().upper()
                        email=request.form['a_email']
                        password=bcrypt.hashpw(request.form['a_password'].encode(), bcrypt.gensalt())

                        sql='INSERT INTO admintb (nombre,apellido,email,password) VALUES (%s,%s,%s,%s)'

                        try:
                            cursor.execute(sql,(nombre,apellido,email,password))
                            conn.commit()

                        except pymysql.err.IntegrityError as e:
                            error_msg = str(e)

                            if "admintb.telefono" in error_msg:
                                flash("El teléfono ingresado ya está registrado.", "error")

                            elif "admintb.email" in error_msg:
                                flash("El correo ingresado ya está registrado.", "error")

                            elif "admintb.documento" in error_msg:
                                flash("El documento ingresado ya está registrado.", "error")

                            else:
                                flash("Ocurrió un error inesperado. Intenta nuevamente.", "error")

                            return redirect(url_for("crear_usuario",id=session['usuario']['id']))

                        finally:
                            conn.close()
                            cursor.close()

                        flash('Usuario - Admin creado exitosamente','usuario')
                        return redirect(url_for('admin',id=session['usuario']['id']))

    return render_template('admin/crear_usuario.html',tipo_usuario=tipo_usuario,hoy=hoy)


################===ADICIONALES===################
#------> Ayuda Al Cliente <----------#
@app.route('/atencion_cliente',methods=('GET','POST'))
def atencion_cliente():
    if request.method=='POST':
        nombre = request.form['nombre'].strip().upper()
        correo = request.form['email']
        motivo = request.form['motivo']
        mensaje = request.form['mensaje'].capitalize

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

    return render_template('otros/atencion_cliente.html')

#--------> Error 404 <----------#
@app.errorhandler(404)
def page_not_found(e):
    return render_template("otros/404.html"), 404


if __name__=='__main__':
    app.run(debug=True)