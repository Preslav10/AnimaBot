class StateManager:
    def __init__(self):
        self.last_detections = []
        self.last_face = None

    def update_detections(self, detections):
        self.last_detections = detections

    def update_face(self, face):
        self.last_face = face