import os
from ml.train_yolo import YOLOTrainer

class AutoRetrain:
    def __init__(self, dataset_path="dataset", threshold=50):
        self.dataset_path = dataset_path
        self.threshold = threshold
        self.last_count = self.count_images()

    def count_images(self):
        total = 0
        for root, _, files in os.walk(self.dataset_path):
            total += len([f for f in files if f.endswith(".jpg")])
        return total

    def check_and_retrain(self):
        current_count = self.count_images()

        if current_count - self.last_count >= self.threshold:
            print("🔁 Стартира автоматично обучение...")

            trainer = YOLOTrainer(self.dataset_path)
            trainer.train()

            self.last_count = current_count

            print("✅ Нов модел е обучен!")
            return True

        return False