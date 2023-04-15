from flask import Flask, jsonify, request
import base64
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Api
from modelos import Base, engine
import Archivo

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'

Base.metadata.create_all(engine)

@app.route('/convertir', methods=['POST'])
def convertir_archivo():
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
    nuevoArchivo = ""
    if (formato_destino == "tar.gz"):
        
        nuevoArchivo = archivo.comprimir_a_tar_gz("mi_archivo.tar.gz")
    elif (formato_destino == "zip"):
       nuevoArchivo=archivo.comprimir_a_zip("mi_archivo.zip")
    return {
        'mensaje': 'El archivo se ha convertido con éxito.',
        'nombre_archivo': nombre_archivo,
        'formato_original': formato_original,
        'formato_destino': formato_destino,
        'base64_Arhivo': nuevoArchivo
    }

@app.route('/saludo', methods=['GET'])
def saludo():
    return "Hola Mundo"
if __name__ == '__main__':
   app.run(host="0.0.0.0")

