from ultralytics import YOLO
import os

class YOLOTrainer:
    def __init__(self, dataset_path="dataset"):
        self.dataset_path = dataset_path

    def generate_yaml(self):
        classes = os.listdir(self.dataset_path)

        with open("dataset.yaml", "w") as f:
            f.write(f"path: {self.dataset_path}\n")
            f.write("train: .\n")
            f.write("val: .\n\n")

            f.write(f"nc: {len(classes)}\n")
            f.write("names: [\n")

            for c in classes:
                f.write(f"  '{c}',\n")

            f.write("]\n")

        print("📄 dataset.yaml създаден")

    def train(self):
        self.generate_yaml()

        model = YOLO("yolov8n.pt")

        model.train(
            data="dataset.yaml",
            epochs=50,
            imgsz=640,
            batch=8
        )

        print("🎯 Обучението приключи!")