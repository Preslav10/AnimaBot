import redis
import json
import base64
import cv2
import numpy as np


class MessageBus:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    # ---------- FRAME (image) ----------
    def send_frame(self, channel, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        data = base64.b64encode(buffer).decode('utf-8')
        self.r.publish(channel, data)

    def receive_frame(self, pubsub):
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message and message['type'] == 'message':
            data = base64.b64decode(message['data'])
            np_arr = np.frombuffer(data, dtype='uint8')
            return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return None

    # ---------- JSON ----------
    def send_json(self, channel, data):
        self.r.publish(channel, json.dumps(data))

    def receive_json(self, pubsub):
        message = pubsub.get_message(ignore_subscribe_messages=True)
        if message and message['type'] == 'message':
            return json.loads(message['data'])
        return None

    # ---------- SUBSCRIBE ----------
    def subscribe(self, channel):
        pubsub = self.r.pubsub()
        pubsub.subscribe(channel)
        return pubsub