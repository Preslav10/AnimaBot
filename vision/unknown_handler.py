from vision.smart_filter import SmartFilter
from vision.dataset_collector import DatasetCollector
from vision.auto_label import AutoLabel
class UnknownHandler:
    def __init__(self, memory):
        self.memory = memory
        self.collector = DatasetCollector()
        self.labeler = AutoLabel()
        self.filter = SmartFilter()

    def handle(self, detection, frame):
        if not self.filter.should_learn(detection, self.memory):
            return

        label = detection["label"]
        bbox = detection.get("bbox")

        print(f"❓ Не съм сигурен какво е това: {label}")
        user_input = input("Какво е това? > ")

        self.memory.save(label, user_input)

        img_path = self.collector.save_unknown(frame, user_input)

        if bbox:
            self.labeler.create_label(img_path, bbox)