import bcrypt

#################### Datos para login Usuarios ####################


#====== PACIENTES ========#
p1={'password':'laurita123',
    'correo':'laura@gmail.com'
}
p2={'password':'calitos0422',
    'correo':'carlosr@gmail.com'
}
p3={'password':'marianatt67',
    'correo':'maria.torres@hotmail.com'
}

p4={
    'password':'jairo',
    'correo':'jairo@gmail.com'
}

p5={
    'password':'qwer',
    'correo':'juankmilobernalz@gmail.com'
}


#====== ADMINS ========#
a1={'password':'robert',
    'correo':'roberto@gmail.com'
}
a2={'password':'jhonessy',
    'correo':'jhonnesy@gmail.com'
}

#====== MEDICOS ========#
m1={'password':'anita03123',
    'correo':'ana.martinez@hospital.com'
}
m2={'password':'luisitocm',
    'correo':'luis.garcia@hospital.com'
}
m3={'password':'ruizofia',
    'correo':'sofia.ruiz@hospital.com'
}

############## Zona de Creacion de passwords ############

hash = bcrypt.hashpw(p5['password'].encode(), bcrypt.gensalt())
        

print(f'esta es tu contra: {hash.decode()}')

