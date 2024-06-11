# Importacion de bibliotecas
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Construccion del aplicativo utilizando el Framework Flask de Python
app = Flask(__name__)
# Configurarle la base de datos
app.config["SQLALCHEMY_DATABASE_URI"]=f"mysql+pymysql://{os.environ.get('MYSQL_USER')}:{os.environ.get('MYSQL_PASS')}@{os.environ.get('MYSQL_USER')}.mysql.pythonanywhere-services.com:3306/{os.environ.get('MYSQL_USER')}$default"
db=SQLAlchemy(app)

# Crear el modelo de la tabla "user"
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    deleted_at = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Crear servicio para la autenticacion de un usuario
@app.route('/login', methods=["POST"])
def login():
    # Obtener los datos de la peticion/request
    if request.is_json:
        data = request.get_json()
        mail = data.get("email")
        pwd = data.get("password")
    else:
        mail = request.form.get("email")
        pwd = request.form.get("password")

    # Hacer una busqueda por nombre de usuario para buscar uno existente
    user=User.query.filter_by(email=mail).first()

    # Preguntar si existe el usuario y
    # validar que la contraseña sea la que tenemos guarada
    if user and user.check_password(pwd):
        return jsonify({"Exito":f"Usuario {user} encontrado"})
    else:
        return jsonify({"Error":"Credenciales inválidas"})

# Servicio de prueba
@app.route('/')
def hello_world():
    return 'Hello from Flask!'