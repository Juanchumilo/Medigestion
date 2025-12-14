import pymysql

#Configuracion de Conexion
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='juan',
        password='2207Chumilo,',
        database='db_medigestion',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )