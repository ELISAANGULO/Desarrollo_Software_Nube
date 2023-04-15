import base64
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify
import hashlib
from flask_restful import Resource
from sqlalchemy import and_, or_
from Archivo import Archivo
from modelos import Usuario, Session, Conversion, ConversionSchema

conversion_schema = ConversionSchema()


class VistaSignIn(Resource):
    def post(self):
        try:
            if (request.json["correo"] is None or request.json["correo"] == ""):
                return "El correo es obligatorio", 400
            session = Session()
            usuario = session.query(Usuario).filter(or_(
                Usuario.correo == request.json["correo"], Usuario.usuario == request.json["usuario"])).first()
            if usuario is None:
                contrasena_encriptada = hashlib.md5(
                    request.json["contrasena"].encode('utf-8')).hexdigest()
                nuevo_usuario = Usuario(
                    usuario=request.json["usuario"], contrasena=contrasena_encriptada, correo=request.json["correo"])
                session.add(nuevo_usuario)
                session.commit()
                # session.close()
                return {"mensaje": "usuario creado exitosamente", "id": nuevo_usuario.id}
            else:
                return "El usuario ya existe", 400
        except Exception as e:
            print("Se presentó el siguiente error", e)


class VistaLogIn(Resource):
    def post(self):
        session = Session()
        contrasena_encriptada = hashlib.md5(
            request.json["contrasena"].encode('utf-8')).hexdigest()
        usuario = session.query(Usuario).filter(or_(Usuario.usuario == request.json["usuario"], Usuario.correo == request.json["usuario"]),
                                                Usuario.contrasena == contrasena_encriptada).first()
        session.commit()
        if usuario is None:
            return "Nombre de usuario o contraseña incorrecta", 400
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id}
