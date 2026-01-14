import pika
import uuid
import json

class Messaging:
    def __init__(self, host='localhost'):
        self.host = host
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()

    def declare_queue(self, queue_name):
        self.channel.queue_declare(queue=queue_name)

    def close(self):
        if self.connection:
            self.connection.close()

class RPCClient(Messaging):
    def __init__(self, host='localhost'):
        super().__init__(host)
        self.callback_queue = None
        self.response = None
        self.corr_id = None

    def connect(self):
        super().connect()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)

    def call(self, routing_key, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message))
        
        while self.response is None:
            self.connection.process_data_events(time_limit=1)
        return self.response

class AsyncPublisher(Messaging):
    def publish(self, routing_key, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            body=json.dumps(message))

class RPCServer(Messaging):
    def __init__(self, queue_name, callback, host='localhost'):
        super().__init__(host)
        self.queue_name = queue_name
        self.callback = callback

    def start(self):
        self.connect()
        self.declare_queue(self.queue_name)
        
        def on_request(ch, method, props, body):
            request_data = json.loads(body)
            print(f" [x] Recieved request: {request_data}")
            
            response = self.callback(request_data)

            ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id=props.correlation_id),
                body=json.dumps(response))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=on_request)

        print(f" [x] Awaiting RPC requests on {self.queue_name}")
        self.channel.start_consuming()
