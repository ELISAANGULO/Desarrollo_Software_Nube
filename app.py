from flask import Flask, jsonify, request
import base64
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_restful import Api
from modelos import Base, engine
import Archivo
from vistas import VistaSignIn, VistaLogIn, VistaConvertir,VistaConversion, VistaFiles, VistaSaludo


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'frase-secreta'

Base.metadata.create_all(engine)
cors = CORS(app)

api = Api(app)
api.add_resource(VistaSignIn, '/api/auth/signup')
api.add_resource(VistaLogIn, '/api/auth/login')
api.add_resource(VistaConvertir, '/api/tasks')
api.add_resource(VistaConversion, '/api/tasks/<int:id_task>')
api.add_resource(VistaFiles, '/api/files/<filename>')
api.add_resource(VistaSaludo, '/saludo')

jwt = JWTManager(app)
if __name__ == '__main__':
   app.run(host="0.0.0.0")

