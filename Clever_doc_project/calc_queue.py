#!/usr/bin/env python

import pika
import uuid

class Calculation(object):

    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue = '', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue = self.callback_queue,
            on_message_callback = self.receive,
            auto_ack = True)

    def receive(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, calcul):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='calc',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(calcul))
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)

calc_request = Calculation()

reponse = calc_request.call("30 - 2")

print("Response : %s" % reponse)
reponse = calc_request.call("30 + 2")

print("Response : %s" % reponse)
reponse = calc_request.call("30 * 2")

print("Response : %s" % reponse)