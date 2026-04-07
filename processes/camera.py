from vision.camera import Camera
from utils.message_bus import MessageBus

def camera_process():
    cam = Camera()
    bus = MessageBus()

    while True:
        frame = cam.get_frame()
        if frame is not None:
            bus.send_frame("camera", frame)