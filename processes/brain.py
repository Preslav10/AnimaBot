import asyncio
import json
from utils.message_bus import MessageBus
from brain.decision_system import DecisionSystem
from brain.state_manager import StateManager

async def brain_loop():
    bus = MessageBus()
    brain = DecisionSystem()
    state = StateManager()

    det_sub = bus.subscribe("detections")
    face_sub = bus.subscribe("face")

    while True:
        det_msg = det_sub.get_message()
        face_msg = face_sub.get_message()

        if det_msg and det_msg['type'] == 'message':
            detections = json.loads(det_msg['data'])
            state.update_detections(detections)

        if face_msg and face_msg['type'] == 'message':
            face_data = json.loads(face_msg['data'])
            state.update_face(face_data)

        actions = brain.decide(state.last_detections, state.last_face)

        for a in actions:
            print(f"🧠 {a}")

        await asyncio.sleep(0.01)

def brain_process():
    asyncio.run(brain_loop())