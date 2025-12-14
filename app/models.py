class Pacientes:
    def __init__(self,nombre,apellido,tipo_documento,documento,fecha_nacimiento,genero,telefono,email,rh,password):
        self.nombre=nombre
        self.apellido=apellido
        self.tipo_documento=tipo_documento
        self.documento=documento
        self.fecha_nacimiento=fecha_nacimiento
        self.genero=genero
        self.telefono=telefono
        self.email=email
        self.rh=rh
        self.password=password

class Especialidades:
    def __init__(self,nombre,descripcion):
        self.nombre=nombre
        self.descripcion=descripcion

class Consultorios:
    def __init__(self,nombre,ubicacion,horario):
        self.nombre=nombre
        self.ubicacion=ubicacion
        self.horario=horario

class Medicos:
    def __init__(self,nombre,apellido,telefono,email):
        self.nombre=nombre
        self.apellido=apellido
        self.telefono=telefono
        self.email=email
        self.especialidad=Especialidades

class Citas:
    def __init__(self,fecha_hora,motivo,estado):
        self.fecha_hora=fecha_hora
        self.motivo=motivo
        self.estado=estado
        self.paciente=Pacientes
        self.medico=Medicos
        self.consultorio=Consultorios

class Historial_Medico:
    def __init__(self,fecha,diagnostico,tratamiento,notas):
        self.fecha=fecha
        self.diagnostico=diagnostico
        self.tratamiento=tratamiento
        self.notas=notas
        self.paciente=Pacientes
        self.medico=Medicos



