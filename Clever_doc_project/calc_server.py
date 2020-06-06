#!/usr/bin/env python

import pika
import sys


class Server(object):

    def __init__(self):
        self.connect()

    def exit(self):
        self.connection.close()
    
    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue = 'calc')

    def calc_request(self, ch, method, props, body):
        self.reponse = eval(body)

        print("[>] Cacul en cours | result : %s" % self.reponse)

        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id=props.correlation_id),
                        body=str(self.reponse))

        print("[>] Envoie de la réponse au client")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def run(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='calc',
                    on_message_callback = self.calc_request)
        
        print(" Waiting Instruction :")

        try:
            self.channel.start_consuming()
        except (KeyboardInterrupt):
            print("Exit")
            self.exit()

if __name__ == "__main__":
    server = Server()
    server.run()