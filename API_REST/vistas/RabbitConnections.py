from google.cloud import pubsub_v1
from google.oauth2 import service_account
from google.oauth2 import service_account
from googleapiclient.discovery import build
class RabbitConnection():
    def __init__(self):
        self.callback=None
        self.publisher= None
        self.topic_id = "DocumentToConvert"
        self.project_id=""
    def crearConexion(self):
        print("xxxxxxxxxxxxxxx  crearConexion xxxxxxxxxx")
        credentials = service_account.Credentials.from_service_account_file(
            'credsub.json')
        service = build('gmail', 'v1', credentials=credentials)
        self.project_id = "amazing-limiter-382016"
        self.topic_id = "DocumentToConvert"
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(
            self.project_id, self.topic_id)

        
    def creacionCola(self, cola):
        print("No necesario trabaja con GPC" + cola)
    
    def enviarMensaje(self, mensaje,cola):

        print("xxxxxxxxxxxxxxx  enviarMensaje xxxxxxxxxx")      
        print(mensaje)

        self.crearConexion()
   
        data = str(mensaje).encode("utf-8")
        # When you publish a message, the client returns a future.
        future = self.publisher.publish(self.topic_path, data)
        print(future.result())
        


    