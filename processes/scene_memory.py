import time
from utils.message_bus import MessageBus


def scene_memory_process():

    bus = MessageBus()

    memory = {}

    sub = bus.subscribe("tracked_objects")

    while True:

        objects = bus.receive_json(sub)

        if objects is None:
            continue

        now = time.time()

        for obj in objects:

            memory[obj["id"]] = {
                "label": obj["label"],
                "bbox": obj["bbox"],
                "last_seen": now
            }

        bus.send_json("scene_memory", memory)