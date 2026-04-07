from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)

    def detect(self, frame):
        results = self.model(frame)
        detections = []

        for r in results:
            for box in r.boxes:
                cls = int(box.cls[0])
                label = self.model.names[cls]
                conf = float(box.conf[0])

                # 🔥 bounding box (YOLO format)
                xywh = box.xywh[0].tolist()  # absolute
                x, y, w, h = xywh

                h_img, w_img, _ = frame.shape

                # нормализиране (YOLO format 0-1)
                x /= w_img
                y /= h_img
                w /= w_img
                h /= h_img

                detections.append({
                    "label": label,
                    "confidence": conf,
                    "bbox": (x, y, w, h)
                })

        return detections