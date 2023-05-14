from flask import Flask
from models import Base, engine
from Listener.ListenerServicioConsulta import ListenerServicioConsulta

app = Flask(__name__)
app.config['SQLALCHEMY_POOL_SIZE'] = 1002
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 1002


Base.metadata.create_all(engine)

@app.teardown_request
def teardown_request(exception=None):
   engine.dispose() # cerrar todas las conexiones de la piscina de SQLAlchemy

listenerServicioConsulta=  ListenerServicioConsulta()
listenerServicioConsulta.listenerConsultaVentas()


