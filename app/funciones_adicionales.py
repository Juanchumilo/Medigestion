from db import get_connection

def contar_usuarios():
    total = contar_pacientes() + contar_medicos() + contar_admins()
    return total

def contar_citas():
    cursor = get_connection().cursor()
    cursor.execute("SELECT COUNT(*) FROM citas")
    total = cursor.fetchone()[0]
    cursor.close()
    return total

def contar_pacientes():
    cursor = get_connection().cursor()
    cursor.execute("SELECT COUNT(*) FROM pacientes")
    total = cursor.fetchone()[0]
    cursor.close()
    return total

def contar_medicos():
    cursor = get_connection().cursor()
    cursor.execute("SELECT COUNT(*) FROM medicos")
    total = cursor.fetchone()[0]
    cursor.close()
    return total

def contar_admins():
    cursor = get_connection().cursor()
    cursor.execute("SELECT COUNT(*) FROM admins")
    total = cursor.fetchone()[0]
    cursor.close()
    return total

def config():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM configuracion_sistema WHERE id=1")
    config = cursor.fetchone()
    conn.close()
    cursor.close()
    return config