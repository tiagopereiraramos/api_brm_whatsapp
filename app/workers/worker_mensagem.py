import pika
import json

def process_message(ch, method, properties, body):
    print(f"Processing message: {json.loads(body)}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    queue_name = "fila_cobrancas"
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_consume(queue=queue_name, on_message_callback=process_message)
    print(f"Worker listening on queue: {queue_name}")
    channel.start_consuming()