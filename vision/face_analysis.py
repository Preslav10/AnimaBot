from deepface import DeepFace

class FaceAnalyzer:
    def analyze(self, frame):
        try:
            result = DeepFace.analyze(
                frame,
                actions=['emotion'],
                enforce_detection=False
            )

            return {
                "emotion": result[0]['dominant_emotion']
            }
        except:
            return None