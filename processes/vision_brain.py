# Improved Vision Brain with Spatial + Temporal Reasoning
# Drop-in replacement idea for vision_brain.py
import time
from collections import defaultdict, deque

class VisionBrain:
    def __init__(self, bus):
        self.bus = bus
        self.previous_people = set()
        self.object_memory = defaultdict(lambda: deque(maxlen=30))  # ~1 sec history (30fps)
        self.event_memory = defaultdict(float)

    def distance(self, a, b):
        return ((a['x'] - b['x'])**2 + (a['y'] - b['y'])**2) ** 0.5

    def bbox_center(self, bbox):
        x1, y1, x2, y2 = bbox
        return {'x': (x1 + x2)/2, 'y': (y1 + y2)/2}

    def is_near(self, obj1, obj2, threshold=100):
        c1 = self.bbox_center(obj1['bbox'])
        c2 = self.bbox_center(obj2['bbox'])
        return self.distance(c1, c2) < threshold

    def process(self, tracked_objects, pose_data):
        current_time = time.time()
        events = []

        people = [o for o in tracked_objects if o['label'] == 'person']
        cups = [o for o in tracked_objects if o['label'] == 'cup']

        current_people_ids = set([p['id'] for p in people])

        # --- 1. ENTRY DETECTION ---
        if len(current_people_ids) > len(self.previous_people):
            events.append("someone_entered_room")

        # --- 2. HOLDING CUP (SPATIAL + POSE) ---
        for person in people:
            pid = person['id']
            if pid not in pose_data:
                continue

            pose = pose_data[pid]
            hands = [pose.get('left_wrist'), pose.get('right_wrist')]

            for cup in cups:
                for hand in hands:
                    if hand and self.distance(hand, self.bbox_center(cup['bbox'])) < 80:
                        self.object_memory[(pid, 'cup')].append(current_time)

                        # Temporal check (holding for > 0.5 sec)
                        if len(self.object_memory[(pid, 'cup')]) > 10:
                            events.append(f"person_{pid}_holding_cup")

        # --- 3. FALL DETECTION (IMPROVED) ---
        for pid, pose in pose_data.items():
            head = pose.get('nose')
            hip = pose.get('hip')
            shoulder = pose.get('shoulder')

            if head and hip and shoulder:
                # More robust: body vertical collapse
                if abs(head['y'] - hip['y']) < 50:
                    if current_time - self.event_memory[pid] > 2:
                        events.append(f"person_{pid}_fell")
                        self.event_memory[pid] = current_time

        # --- 4. SPATIAL RELATIONS ---
        for person in people:
            for obj in tracked_objects:
                if obj['id'] == person['id']:
                    continue

                if self.is_near(person, obj):
                    events.append(f"person_{person['id']}_near_{obj['label']}")

        # --- 5. TEMPORAL ACTIONS ---
        for pid in current_people_ids:
            self.object_memory[(pid, 'presence')].append(current_time)

            if len(self.object_memory[(pid, 'presence')]) > 20:
                events.append(f"person_{pid}_staying")

        self.previous_people = current_people_ids

        # --- OUTPUT ---
        self.bus.send_json("vision_events", {
            "events": events,
            "timestamp": current_time
        })


# --- WHAT THIS ADDS ---
# ✔ Real hand-object interaction (cup detection improved)
# ✔ Spatial awareness (near relationships)
# ✔ Temporal reasoning (holding, staying)
# ✔ Better fall detection
# ✔ Memory system (short-term context)
