from ml.auto_retrain import AutoRetrain
from utils.message_bus import MessageBus

def retrain_process():
    auto = AutoRetrain()
    bus = MessageBus()

    while True:
        if auto.check_and_retrain():
            bus.send_json("model_update", {"status": "updated"})