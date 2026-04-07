from vision.face_analysis import FaceAnalyzer
from utils.message_bus import MessageBus

def face_process():
    bus = MessageBus()
    analyzer = FaceAnalyzer()

    pubsub = bus.subscribe("camera")

    while True:
        frame = bus.receive_frame(pubsub)
        if frame is not None:
            face_data = analyzer.analyze(frame)
            bus.send_json("face", face_data)