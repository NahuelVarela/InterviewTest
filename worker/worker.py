import pika
import json

from database import(
	CreateEntry,
	UpdateEntry,
	DeleteEntry
)

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
	pika.ConnectionParameters(
		host='localhost',
		port='5672',
		credentials=credentials
		)
	)
channel = connection.channel()
channel.queue_declare(queue='primary', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch,method,properties,body):
	data = json.loads(body.decode())
	print(" [x] Received %s on entry %s",data["action"],data["id"])
	if data["action"] == "create":
		CreateEntry(data)
	elif data["action"] == "update":
		UpdateEntry(data)
	else:
		DeleteEntry(data)
	print(" [x] Done")
	ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='primary', on_message_callback=callback)
channel.start_consuming()