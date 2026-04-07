class AutoLabel:
    def create_label(self, image_path, bbox, class_id=0):
        """
        bbox = (x_center, y_center, width, height) в YOLO формат (0-1)
        """

        label_path = image_path.replace(".jpg", ".txt")

        x, y, w, h = bbox

        with open(label_path, "w") as f:
            f.write(f"{class_id} {x} {y} {w} {h}")

        print(f"🏷️ Реален label създаден: {label_path}")