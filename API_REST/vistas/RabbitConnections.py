import pika
import aio_pika
class RabbitConnection():
    def __init__(self):
        self.rabbitmq_host = '34.138.120.16'
        self.rabbitmq_port = 5672
        self.rabbitmq_username = 'admin'
        self.rabbitmq_password = 'admin'
        self.connection = None
        self.callback=None
    def crearConexion(self):
        parameters = pika.ConnectionParameters(
            self.rabbitmq_host, self.rabbitmq_port, '/', pika.PlainCredentials(username=self.rabbitmq_username, password=self.rabbitmq_password),heartbeat=0)
        self.connection = pika.BlockingConnection(parameters)
        return self.connection
        
    def creacionCola(self, cola):
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=cola)
        return self.channel
    
    def enviarMensaje(self, cola, mensaje):
        self.crearConexion
        self.creacionCola(cola)
        self.channel.basic_publish(
            exchange='', routing_key=cola, body=f'{mensaje}')
        print(f'Conversion enviada   {mensaje}')
        self.cerrarConexion()
        
    def cerrarConexion(self):
        self.channel.stop_consuming()
        self.connection.close()

    def crearListener(self, cola):
        #self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue=cola, on_message_callback=self.callback, auto_ack=False)
        self.channel.start_consuming()
    
    def publishMessage(self, id, cola):
        try:
            self.crearConexion()
            channel = self.connection.channel()
            channel.queue_declare(queue= "DocumentToConvert")
            channel.basic_publish(exchange='', routing_key='DocumentToConvert', body=f"{id}")
            self.connection.close()
        except Exception as e:
            print("Se presentó el siguiente error", e)

    