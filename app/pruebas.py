from flask import Flask, render_template, request, redirect,flash
from db import get_connection
import models
import bcrypt
import os

import bcrypt

#====== PACIENTES ========#
p1='laurita123'
p2='calitos0422'
p3='marianatt67'
p4='joselin'
p5='juanito'
p6='estevan'
p7='london'

#====== ADMINS ========#
a1='robert'
a2='jhonessy'

#====== MEDICOS ========#
m1='anita03123'
m2='luisitocm'
m3='ruizofia'


hash = bcrypt.hashpw(p6.encode(), bcrypt.gensalt())

        

print(f'esta es tu contra: {hash.decode()}')

