import redis
import json
import base64
import cv2
import numpy as np  # <- добави това

class MessageBus:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)

    def send_frame(self, channel, frame):
        _, buffer = cv2.imencode('.jpg', frame)
        data = base64.b64encode(buffer).decode('utf-8')
        self.r.publish(channel, data)

    def receive_frame(self, pubsub):
        message = pubsub.get_message()
        if message and message['type'] == 'message':
            data = base64.b64decode(message['data'])
            np_arr = np.frombuffer(data, dtype='uint8')  # вече работи
            return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return None

    def send_json(self, channel, data):
        self.r.publish(channel, json.dumps(data))

    def subscribe(self, channel):
        pubsub = self.r.pubsub()
        pubsub.subscribe(channel)
        return pubsub