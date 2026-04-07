import json
from vision.object_detection import ObjectDetector
from utils.message_bus import MessageBus

def detection_process():
    bus = MessageBus()
    detector = ObjectDetector()

    pubsub = bus.subscribe("camera")
    model_sub = bus.subscribe("model_update")

    while True:
        # reload model if needed
        msg = model_sub.get_message()
        if msg and msg['type'] == 'message':
            detector = ObjectDetector("runs/detect/train/weights/best.pt")

        frame = bus.receive_frame(pubsub)
        if frame is not None:
            detections = detector.detect(frame)
            bus.send_json("detections", detections)
            bus.send_frame("frames", frame)