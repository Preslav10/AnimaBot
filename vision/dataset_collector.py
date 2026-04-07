import os
import cv2
import time

class DatasetCollector:
    def __init__(self, base_path="dataset"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def save_unknown(self, frame, label_hint="unknown"):
        timestamp = int(time.time() * 1000)
        folder = os.path.join(self.base_path, label_hint)

        os.makedirs(folder, exist_ok=True)

        filename = os.path.join(folder, f"{timestamp}.jpg")
        cv2.imwrite(filename, frame)

        print(f"📸 Запазено изображение: {filename}")

        return filename  # 🔥 ВРЪЩАМЕ ПЪТЯ