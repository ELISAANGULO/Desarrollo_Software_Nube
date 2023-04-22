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
                session.close()
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
        session.close()
        if usuario is None:
            return "Nombre de usuario o contraseña incorrecta", 400
        else:
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso, "id": usuario.id}
        
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
        data = request.get_json()
        nombre_archivo = data['nombre_archivo']
        formato_original = data['formato_original']
        formato_destino = data['formato_destino']
        base64_Arhivo = data['base64_Arhivo']

        archivo_bytes = base64.b64decode(base64_Arhivo)
        # Escribir los bytes en un archivo
        with open(nombre_archivo, 'wb') as f:
            f.write(archivo_bytes)
        archivo = Archivo(nombre_archivo)
        nuevoArchivo=""
        if (formato_destino == "pdf"):
            nuevoArchivo = archivo.comprimir_a_tar_gz("mi_archivo.tar.gz")
        elif (formato_destino == "tar.gz"):
            nuevoArchivo=archivo.comprimir_a_tar_gz("mi_archivo.tar.gz")
        elif (formato_destino == "zip"):
            nuevoArchivo=archivo.comprimir_a_zip("mi_archivo.zip")
        elif (formato_destino == "7z"):
            nuevoArchivo=archivo.comprimir_a_7z("mi_archivo.7z")
        session = Session()
        conversion_exist = session.query(Conversion).filter(and_(Conversion.usuario_id ==get_jwt_identity(), Conversion.disponible == True, Conversion.archivo_base == base64_Arhivo, Conversion.nombre_archivo == nombre_archivo, Conversion.extension_original == formato_original, Conversion.extension_destino == formato_destino)).first()
        if(conversion_exist is None):
            conversion = Conversion(nombre_archivo =nombre_archivo, archivo_base = base64_Arhivo, extension_original = formato_original, extension_destino = formato_destino, archivo_convertido = nuevoArchivo, disponible = True, usuario_id = get_jwt_identity(), fecha_subida = datetime.now(), status = "processed")
            session.add(conversion)
        else:
            conversion_exist.fecha_subida = datetime.now()
        session.commit()
        session.close()
        

        return {
            'mensaje': 'El archivo se ha convertido con éxito.',
            'nombre_archivo': nombre_archivo,
            'formato_original': formato_original,
            'formato_destino': formato_destino,
            'base64_Arhivo': nuevoArchivo
        }

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
    @jwt_required()
    def get(self):
        return "Hola Mundo"

class VistaFiles(Resource):
    @jwt_required()
    def get(self, filename):
        session = Session()
        conversion = session.query(Conversion).filter(and_(Conversion.usuario_id ==get_jwt_identity(), Conversion.disponible == True, Conversion.nombre_archivo == filename)).first()
        if(conversion is None):
            return {"message" : f"La tarea de conversión con nombre: {filename}, no existe o no tiene autorización para acceder a ella"}, 409
        response = {"nombre_archivo" : f"{conversion.nombre_archivo}", "archivo_original" : f"{conversion.archivo_base}", "archivo_procesado" : f"{conversion.archivo_convertido}"}
        session.close()
        return response
