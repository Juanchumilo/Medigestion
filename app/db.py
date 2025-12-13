import pymysql

#Configuracion de Conexion
def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='juan',
        password='2207Chumilo,',
        database='db_medigestion',
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )