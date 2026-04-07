class DecisionSystem:
    def decide(self, detections, face_data):
        actions = []

        for d in detections:
            label = d["label"]
            conf = d["confidence"]

            if conf < 0.5:
                actions.append(f"🔍 Проверка на обект: {label}")

            if label in ["knife", "fire"]:
                actions.append("⚠️ Опасност засечена!")

        if face_data:
            emotion = face_data.get("emotion")

            if emotion == "angry":
                actions.append("😟 Човекът е ядосан")
            elif emotion == "happy":
                actions.append("😊 Човекът е щастлив")

        return actions