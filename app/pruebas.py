from flask import Flask, render_template, request, redirect,flash
from db import get_connection
import models
import bcrypt
import os

import bcrypt
p1='laurita123'
p2='calitos0422'
p3='marianatt67'
a1='robert'
a2='jhonessy'
m1='anita03123'
m2='luisitocm'
m3='ruizofia'


hash = bcrypt.hashpw(m2.encode(), bcrypt.gensalt())
lista=[(1,2,3),(4,5,6)]
conteo=0
conteo2=-1
while conteo!=len(lista):
    conteo+=1
    for i in lista:
        print(lista[0+1])
        

print(f'esta es tu contra: {hash.decode()}')

