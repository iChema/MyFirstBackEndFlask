# Importación de bibliotecas
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import User

# Construcción del aplicativo utilizando el Framework Flask de Python
app = Flask(__name__)

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.environ.get('MYSQL_USER')}:{os.environ.get('MYSQL_PASS')}@{os.environ.get('MYSQL_USER')}.mysql.pythonanywhere-services.com:3306/{os.environ.get('MYSQL_USER')}$default"
db = SQLAlchemy(app)


# Crear servicio para la autenticación de un usuario
@app.route('/login', methods=["POST"])
def login():
    if request.is_json:
        data = request.get_json()
        mail = data.get("email")
        pwd = data.get("password")
    else:
        mail = request.form.get("email")
        pwd = request.form.get("password")

    user = User.query.filter_by(email=mail).first()

    if user and user.check_password(pwd):
        return jsonify({"Exito": f"Usuario {user.name} encontrado"})
    else:
        return jsonify({"Error": "Credenciales inválidas"})

# Servicio de prueba
@app.route('/')
def hello_world():
    return 'Hello from Flask!'

# Crear usuario
@app.route('/users', methods=["POST"])
def create_user():
    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        mail = data.get("email")
        pwd = data.get("password")
    else:
        name = request.form.get("name")
        mail = request.form.get("email")
        pwd = request.form.get("password")

    if name and mail and pwd:
        user = User(name=name, email=mail)
        user.set_password(pwd)
        db.session.add(user)
        db.session.commit()
        return jsonify({"Exito": f"Usuario {user.name} creado correctamente"})
    else:
        return jsonify({"Error": "Datos incompletos"})

# Obtener usuarios
@app.route('/users', methods=["GET"])
def get_users():
    users = User.query.filter_by(deleted_at=None).all()
    result = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at
        }
        for user in users
    ]
    return jsonify(result)

# Obtener usuario por ID
@app.route('/users/<int:id>', methods=["GET"])
def get_user_by_id(id):
    user = User.query.filter_by(id=id, deleted_at=None).first_or_404()
    result = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }
    return jsonify(result)

# Eliminar usuario
@app.route('/users/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = User.query.get_or_404(id)
    if user:
        user.deleted_at = datetime.now()
        # db.session.delete(user)  # Para borrado físico
        db.session.commit()
        return jsonify({"Exito": "Usuario eliminado"})
    else:
        return jsonify({"Error": "Usuario no encontrado"})

# Actualizar usuario
@app.route('/users/<int:id>', methods=["PUT"])
def update_user(id):
    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        mail = data.get("email")
        pwd = data.get("password")
    else:
        name = request.form.get("name")
        mail = request.form.get("email")
        pwd = request.form.get("password")

    user = User.query.get_or_404(id)

    if name:
        user.name = name

    if mail:
        user.email = mail

    if pwd:
        if not user.check_password(pwd):
            user.set_password(pwd)
        else:
            return jsonify({"Error": "No puedes guardar la misma contraseña"})

    db.session.commit()
    return jsonify({"Exito": f"Usuario {user.name} actualizado correctamente"})

if __name__ == '__main__':
    app.run(debug=True)
