import pymysql

#Configuracion de Conexion
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='2207Chumilo,',
        database='DB_MEDIGESTION',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )