import pika

# PLANET radamar:mercury
params = pika.URLParameters('amqp://guest:guest@10.10.10.190:5672')
connection = pika.BlockingConnection(params)

channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

