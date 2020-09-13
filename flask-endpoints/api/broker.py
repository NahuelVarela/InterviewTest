import pika
import json

def sendMessage(queue,body):
	credentials = pika.PlainCredentials('guest', 'guest')
	connection = pika.BlockingConnection(pika.ConnectionParameters(
		host='localhost',
		port='5672',
		credentials=credentials
		)
	)
	channel = connection.channel()
	channel.queue_declare(queue=queue,durable=True)
	channel.basic_publish(exchange='',
                      routing_key=queue,
                      body=json.dumps(body))
	connection.close()