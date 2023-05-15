from datetime import datetime
import threading
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify
import hashlib
from flask_restful import Resource
from sqlalchemy import and_, or_
from vistas.RabbitConnections import RabbitConnection
from modelos import Usuario, Session, Conversion, ConversionSchema,UsuarioSchema
import random
usuario_schema = UsuarioSchema
conversion_schema = ConversionSchema()
rabbit_connection = RabbitConnection()


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
                session.close()
                return {"mensaje": "usuario creado exitosamente", "id": nuevo_usuario.id}
            else:
                return "El usuario ya existe", 400
        except Exception as e:
            print("Se presentó el siguiente error", e)


class VistaLogIn(Resource):
    def post(self):
        try:
            session = Session()
            contrasena_encriptada = hashlib.md5(
                request.json["contrasena"].encode('utf-8')).hexdigest()
            usuario = session.query(Usuario).filter(or_(Usuario.usuario == request.json["usuario"], Usuario.correo == request.json["usuario"]),
                                                    Usuario.contrasena == contrasena_encriptada).first()
            session.close()
            if usuario is None:
                return "Nombre de usuario o contraseña incorrecta", 400
            else:
                token_de_acceso = create_access_token(identity=usuario.id)
                return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id}
        except Exception as e:
            print("Se presentó el siguiente error: ", e)

class VistaConvertir(Resource):
    @jwt_required()
    def get(self):
        session = Session()
        conversiones = session.query(Conversion).filter(and_(Conversion.usuario_id ==get_jwt_identity(), Conversion.disponible == True)).all()
        result = conversion_schema.dump(conversiones, many=True)
        session.close()
        return jsonify(result)
    
    @jwt_required()
    def post(self):
        try:
            usuario_id = get_jwt_identity()
            data = request.get_json()
            nombre_archivo = data['nombre_archivo']
            formato_original = data['formato_original']
            formato_destino = data['formato_destino']
            base64_Arhivo = data['base64_Arhivo']
            fileForGCP="myFile"+ str (random.randint(0, 9999999))+"."+ formato_destino
            nombre_original_gcp = nombre_archivo.split(".")[0] + str (random.randint(0, 9999999))+"."+formato_original
            conversion = Conversion(nombre_archivo_original = nombre_archivo, 
                                    nombre_archivo_original_gcp = nombre_original_gcp,
                                    nombre_archivo_convertido_gcp = fileForGCP,
                                    archivo_base64_original = base64_Arhivo, 
                                    extension_original = formato_original, 
                                    extension_destino = formato_destino,
                                    disponible = False, 
                                    usuario_id = usuario_id,
                                    fecha_subida = datetime.now(), 
                                    status = "uploaded")
            myThreadSave = threading.Thread(
            target= SaveConvertion, args=(conversion, ""))
            myThreadSave.start()
            conver = {"nombre_archivo_original" : nombre_archivo,
                      "nombre_archivo_original_gcp" : nombre_original_gcp,
                      "nombre_archivo_convertido_gcp": fileForGCP,
                      "usuario_id": usuario_id}
            
            
            myThread = threading.Thread(
                 target=rabbit_connection.enviarMensaje, args=(str( conver), ""))
            myThread.start()
            return {
                'mensaje': 'El archivo ha sido cargado con exito, podrá acceder a él en algunos minutos'
            }
        except Exception as e:
            print("Se presentó el siguiente error: ", e)

def SaveConvertion(conversion, cola):
    session = Session()
    session.add(conversion)
    session.commit()
    session.close()

class VistaConversion(Resource):
    @jwt_required()
    def get(self, id_task):
        session = Session()
        conversion = session.query(Conversion).filter(and_(Conversion.usuario_id ==get_jwt_identity(), Conversion.disponible == True, Conversion.id == id_task)).first()
        if(conversion is None):
            return {"message" : f"La tarea de conversión con id: {id_task}, no existe o no tiene autorización para verla"}, 409
        result = conversion_schema.dump(conversion)
        session.close()
        return jsonify(result)
    
    @jwt_required()
    def delete(self, id_task):
        session = Session()
        conversion = session.query(Conversion).filter(and_(Conversion.usuario_id ==get_jwt_identity(), Conversion.disponible == True, Conversion.id == id_task)).first()
        if(conversion is None):
            return {"message" : f"La tarea de conversión con id: {id_task}, no existe o no tiene autorización para acceder a ella"}, 409
        session.delete(conversion)
        session.close()
        return 204
    
class VistaSaludo(Resource):
    def get(self):
        return "Hola Mundo"

class VistaFiles(Resource):
    @jwt_required()
    def get(self, filename):
        session = Session()
        conversion = session.query(Conversion).filter(and_(Conversion.usuario_id ==get_jwt_identity(), Conversion.disponible == True, Conversion.nombre_archivo_original_gcp == filename)).first()
        if(conversion is None):
            return {"message" : f"La tarea de conversión con nombre: {filename}, no existe o no tiene autorización para acceder a ella"}, 409
        if conversion.status != "processed":
            return {"message" : f"La tarea de conversión con nombre: {filename}, aún no ha sido procesada"}, 409
        base_url_original_gcp = "https://storage.googleapis.com/desarrollocloud2018461201106/Originales/"
        base_url_convertido_gcp = "https://storage.googleapis.com/desarrollocloud2018461201106/Convertidos/"
        url_archivo_original = base_url_original_gcp + conversion.nombre_archivo_original_gcp
        url_archivo_convertido = base_url_convertido_gcp + conversion.nombre_archivo_convertido_gcp
        response = {"nombre_archivo" : conversion.nombre_archivo_original, "url_archivo_original" : url_archivo_original, "url_archivo_convertido" : url_archivo_convertido}
        session.close()
        return response