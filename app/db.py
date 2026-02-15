import pymysql

#Configuracion de Conexion

def get_connection():
    try:
        return pymysql.connect(
        host='localhost',
        user='root',
        password='2207Chumilo,',
        database='db_medigestion',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print("Error de conexión a la base de datos:", e)
        return None
