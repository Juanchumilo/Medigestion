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

password_plana = a2   # aquí pones la contraseña que quieras hashear
hash = bcrypt.hashpw(password_plana.encode(), bcrypt.gensalt())

print(f'esta es tu contra: {hash.decode()}')

