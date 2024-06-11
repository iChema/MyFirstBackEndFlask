# Aplicación Flask en PythonAnywhere

Este repositorio contiene una simple aplicación Flask desplegada en [PythonAnywhere](https://www.pythonanywhere.com/). 
Creamos una cuenta gratuita en PythonAnywhere, configuramos una aplicación Flask y la conectamos a una base de datos MySQL proporcionada por la plataforma.

## Comenzando

### 1. Crear una Cuenta Gratuita en PythonAnywhere

1. Ve a [PythonAnywhere](https://www.pythonanywhere.com/).
2. Regístrate para obtener una cuenta gratuita.

### 2. Configurar la Aplicación Flask

1. Inicia sesión en tu cuenta de PythonAnywhere.
2. Ve a la pestaña "Web" y haz clic en "Add a new web app".
3. Elige "Flask" como el framework y sigue las instrucciones para crear la aplicación.

### 3 Crear el Ambiente Virtual de python

1. Correr el siguiente comando en el bash

'''shell
mkvirtualenv myvirtualenv
'''

2. Ve a la pestaña "Web", en la sección "Virtualenv:" copia esta url "/home/tu_usuario/.virtualenvs/myvirtualenv"

### 4. Editar la Aplicación

1. Navega a la pestaña "Files" en PythonAnywhere.
2. Abre el archivo llamado `flask_app.py` y reemplaza su contenido con el código proporcionado en este repositorio.

### 5. Configurar la Base de Datos MySQL

1. PythonAnywhere proporciona una instancia de MySQL que puedes usar.
2. Ve a la pestaña "Databases" para encontrar tus credenciales de la base de datos MySQL.
3. Ejecutamos el siguiente código SQL para crear una tabla de ejemplo

''' sql
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

### 6. Crear el Archivo `.env`

Crea un archivo `.env` en el directorio raíz de tu aplicación Flask para almacenar tus credenciales de MySQL de forma segura. El archivo `.env` debería verse algo así:

'''python
MYSQL_USER='tu_usuario_mysql'
MYSQL_PASS='tu_contraseña_mysql'
'''

### 7. Cargar el archvio de varibales de entorno

Editar el archivo 'tu_usuario_pythonanywhere_com_wsgi.py' en la ruta '/var/www/tu_usuario_pythonanywhere_com_wsgi.py'

'''python
import sys
import os
from dotenv import load_dotenv

# add your project directory to the sys.path
project_home = '/home/tu_usuario/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Cargar las variables de entorno
load_dotenv(os.path.join(project_home, '.env'))

# Establecer el entorno de Flask
os.environ['FLASK_APP'] = 'flask_app.py'

# import flask app but need to call it "application" for WSGI to work
from flask_app import app as application  # noqa
'''

### 8. Instar dependencias

'''shell
pip install flask
pip install flask_sqlalchemy
pip install pymysql
pip install python-dotenv
'''