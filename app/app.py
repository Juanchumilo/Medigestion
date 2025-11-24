from flask import Flask,render_template,request
import pymysql

app=Flask(__name__)

#Configuracion de Conexion
connection=pymysql.connect(
    host='localhost',
    user='root',
    password='2207Chumilo,',
    database='DB_MEDIGESTION',
    port=3306,
    cursorclass=pymysql.cursors.DictCursor
)

#Index
@app.route('/')
def index():
    return render_template('index.html')

#Paciente
#@app.route('/Paciente/<int:id_Paciente>')
#def Paciente(id_Paciente):
    #return render_template('paciente.html')


#Error 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__=='__main__':
    app.run(debug=True,port=5001)