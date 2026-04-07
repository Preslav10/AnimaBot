# processes/pose.py

from ultralytics import YOLO
import time

model = YOLO("yolov8n-pose.pt")  # автоматично ще се свали

def pose_process(bus):
    print("[POSE] Started with YOLOv8 Pose")

    while True:
        msg = bus.receive("frames")
        if msg is None:
            continue

        frame = msg["frame"]
        tracked_objects = msg.get("tracked_objects", [])

        results = model(frame, verbose=False)

        pose_data = {}

        if len(results) > 0:
            r = results[0]

            if r.keypoints is not None:
                keypoints = r.keypoints.xy.cpu().numpy()

                # Свързваме pose с tracking (по bbox proximity)
                for i, person_kps in enumerate(keypoints):
                    best_match_id = None
                    best_dist = 99999

                    for obj in tracked_objects:
                        if obj["label"] != "person":
                            continue

                        x1, y1, x2, y2 = obj["bbox"]
                        cx = (x1 + x2) / 2
                        cy = (y1 + y2) / 2

                        # използваме nose като reference
                        nose = person_kps[0]
                        dist = ((nose[0] - cx)**2 + (nose[1] - cy)**2)**0.5

                        if dist < best_dist:
                            best_dist = dist
                            best_match_id = obj["id"]

                    if best_match_id is None:
                        continue

                    # YOLO keypoints mapping
                    pose_data[best_match_id] = {
                        "nose": {"x": float(person_kps[0][0]), "y": float(person_kps[0][1])},
                        "left_eye": {"x": float(person_kps[1][0]), "y": float(person_kps[1][1])},
                        "right_eye": {"x": float(person_kps[2][0]), "y": float(person_kps[2][1])},
                        "left_shoulder": {"x": float(person_kps[5][0]), "y": float(person_kps[5][1])},
                        "right_shoulder": {"x": float(person_kps[6][0]), "y": float(person_kps[6][1])},
                        "left_wrist": {"x": float(person_kps[9][0]), "y": float(person_kps[9][1])},
                        "right_wrist": {"x": float(person_kps[10][0]), "y": float(person_kps[10][1])},
                        "hip": {
                            "x": float((person_kps[11][0] + person_kps[12][0]) / 2),
                            "y": float((person_kps[11][1] + person_kps[12][1]) / 2),
                        },
                        "shoulder": {
                            "x": float((person_kps[5][0] + person_kps[6][0]) / 2),
                            "y": float((person_kps[5][1] + person_kps[6][1]) / 2),
                        }
                    }

        bus.send_json("pose", pose_data)