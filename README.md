# Medigestion

Medigestion es un Proyecto personal del tecnologo Analisis y Desarrollo de Software del SENA Colombia. 
El proyecto consiste en una app web que tenga como funcion la gestion de citas medicas. 

## Dependencias
Medigestion esta hecho con 3 lenguajes: HTML,CSS y python-flask.
Las dependencias que deben ser descargadas son:

-- Python
-- Flask
-- bcrypt
-- datetime
-- pymysql
-- MYSQL 
-- jwt

Todas estas dependencias deben ser instaladas en un entorno virtual preferiblemente (ojalá que sea fuera de la carpeta Medigestion/), como sugerencia personal recomiendo venv, ya que viene instalado con python.

### 🚀 Instalación

```bash
git clone https://github.com/Juanchumilo/Medigestion.git
cd Medigestion
```

#### Pasos a seguir
En la carpeta Medigestion/DB_MEDIGESTION/ encontrará el archivo .sql base con algunos usuarios y citas ya creadas (db de pruebas) esta podrá usarla para comprobar las funcionalidades del Aplicativo. Al importar la db en su sistema DEBERÁ asegurarse de que el archivo en Medigestion/app/ llamado db.py, esté configurado para el nombre del root de la conexion de su MYSQL, el nombre de la db (si decidió el cambiarla) y la contraseña, estos son los obligatorios, ya si cambió el puerto o el nombre del host (localhost por defecto) debera hacerlo coincidir para una optima conexion del Aplicativo a la db.

Por ultimo debe ir al editor de codigo o donde se prefiera ejecutar el entorno virual con las dependencias, y alli ejecutar el archivo app.py  De ésta manera: "python [ruta del archivo app.py]", por defecto y si se sigue la indicacion de crear el entorno virtual fuera de la carpeta Medigestion la ruta será: .\Medigestion\app\app.py

Con eso el Aplicativo sera ejecutado completamente.


# Nota
Para saber las contraseñas de los usuarios, estas estarán en el archivo pruebas.py



