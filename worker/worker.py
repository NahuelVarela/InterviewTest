import pika
import json
import requests

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
	reception = " [x] Received {} on entry {}".format(data[1]["action"],data[0]["id"])
	print(reception)
	if data[1]["action"] == "create":
		CreateEntry(data)
	elif data[1]["action"] == "update":
		UpdateEntry(data)
	else:
		DeleteEntry(data)
	completed = " [x] Task {} completed".format(data[1]["task-id"])
	print(completed)
	sendRequest(data[1])
	ch.basic_ack(delivery_tag=method.delivery_tag)

def sendRequest(task_information):
	""" Basic PUT request to the webhook server for completed tasks"""
	python_webhook_server = "http://127.0.0.1:3000/tasks"
	r = requests.put(python_webhook_server,json={"Task-id":task_information["task-id"],"Status": "Completed"})

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='primary', on_message_callback=callback)
channel.start_consuming()