from flask import Flask, render_template, request, redirect
from db import get_connection
import models

app=Flask(__name__)

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
    app.run(debug=True)