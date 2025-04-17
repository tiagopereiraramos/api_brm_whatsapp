import json

import pika
from config.config import getenv
from util.dataclass import Cadastro
import requests
from urllib.parse import urlparse


class RabbitService:
    def __init__(self, rabbitmq_url: str = f"{getenv('RABBITMQ_URL')}"):
        rabbitmq_url = getenv("RABBITMQ_URL")
        self.rabbitmq_url = rabbitmq_url
        parsed_url = urlparse(rabbitmq_url)
        self.username = parsed_url.username or "guest"
        self.password = parsed_url.password or "guest"
        self.rabbitmq_api_url = f"http://{parsed_url.hostname}:15672/api"
        self.auth = (self.username, self.password)

    def get_channel(self):
        connection = pika.BlockingConnection(
            pika.URLParameters(self.rabbitmq_url))
        return connection, connection.channel()

    def list_queues(self):
        response = requests.get(
            f"{self.rabbitmq_api_url}/queues", auth=self.auth)
        if response.status_code == 200:
            return [queue["name"] for queue in response.json()]
        return []

    def purge_queues(self):
        connection, channel = self.get_channel()
        queues = self.list_queues()
        for queue in queues:
            try:
                channel.queue_purge(queue)
                print(f"Queue '{queue}' purged successfully.")
            except pika.exceptions.ChannelClosedByBroker:
                print(f"Failed to purge queue '{queue}'.")
        connection.close()

    def delete_queues(self):
        connection, channel = self.get_channel()
        queues = self.list_queues()
        for queue in queues:
            try:
                channel.queue_delete(queue)
                print(f"Queue '{queue}' deleted successfully.")
            except pika.exceptions.ChannelClosedByBroker:
                print(f"Failed to delete queue '{queue}'.")
        connection.close()

    def delete_queue(self, queue_name: str):
        connection, channel = self.get_channel()
        try:
            channel.queue_delete(queue_name)
            print(f"Queue '{queue_name}' deleted successfully.")
        except pika.exceptions.ChannelClosedByBroker:
            print(f"Failed to delete queue '{queue_name}'.")
        connection.close()

    def queue_exists(self, channel, queue_name: str) -> bool:
        try:
            channel.queue_declare(queue=queue_name, passive=True)
            return True
        except pika.exceptions.ChannelClosedByBroker:
            return False

    def producer(
        self,
        objetos: list[str] | str,
        rabbitmq_url: str = "amqp://guest:guest@localhost:5672/",
    ) -> None:
        connection = pika.BlockingConnection(
            pika.URLParameters(self.rabbitmq_url))
        channel = connection.channel()
        if isinstance(objetos, str):
            objetos = [objetos]
        
        for obj in objetos:
            queue_name = getenv("RABBITMQ_QUEUE")
            if not self.queue_exists(channel, queue_name):
                channel = connection.channel()
                channel.queue_declare(queue=queue_name, durable=True)

            message = json.dumps(obj)

            channel.basic_publish(
                exchange="",
                routing_key=queue_name,
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
            print(f"Sent message to queue '{queue_name}': {message}")

        connection.close()
