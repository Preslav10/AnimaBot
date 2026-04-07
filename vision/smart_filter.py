class SmartFilter:
    def __init__(self, conf_threshold=0.6):
        self.conf_threshold = conf_threshold

    def should_learn(self, detection, memory):
        label = detection["label"]
        confidence = detection["confidence"]

        # ❌ ако вече го знае добре → skip
        if memory.exists(label) and confidence > 0.8:
            return False

        # ✅ ако е ново или несигурно → учи
        if confidence < self.conf_threshold:
            return True

        if not memory.exists(label):
            return True

        return False