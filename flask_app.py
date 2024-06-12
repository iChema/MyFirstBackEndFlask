# Importacion de bibliotecas
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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

# Crear usuario
@app.route('/create_user',methods=["POST"])
def create_user():
    # Obtener los datos
    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        mail = data.get("email")
        pwd = data.get("password")
    else:
        name = request.form.get("name")
        mail = request.form.get("email")
        pwd = request.form.get("password")

    # Verificar si hay datos para agregar y
    # crear el usuario en la base de datos
    if name and mail and pwd:
        user = User(name = name,email = mail)
        user.set_password(pwd)
        db.session.add(user)
        db.session.commit()
        return jsonify({"Exito":f"Usuario {user.name} creado correctamente"})
    else:
        jsonify({"Error":"Datos incompletos"})

@app.route ('/get_users', methods=["GET"])
def get_users():
    # Traer usuarios
    users = User.query.filter_by(deleted_at = None).all()
    result = [
        {
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "created_at":user.created_at
        }
        for user in users
        ]
    return jsonify(result)

@app.route ('/get_user_by_id/<int:id>', methods=["GET"])
def get_user_by_id(id):
    # Traer usuario
    # Cuando no se usa borrado lógico
    #user = User.query.get_or_404(id)
    user = User.query.filter_by(id = id,deleted_at = None).first_or_404()
    result = {
            "id":user.id,
            "name":user.name,
            "email":user.email,
            "created_at":user.created_at
        }
    return jsonify(result)

@app.route ('/delete_user/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    if user:
        # Borrado lógico
        user.deleted_at = datetime.now()
        # Borrado físico
        #db.session.delete(user)

        db.session.commit()
        return jsonify({"Exito":"Usuario eliminado"})
    else:
        return jsonify({"Error":"Usuario no encontrado"})