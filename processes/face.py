# processes/face.py

import insightface
import numpy as np

app = insightface.app.FaceAnalysis()
app.prepare(ctx_id=-1)

def face_process(bus):
    print("[FACE] Started with InsightFace")

    while True:
        msg = bus.receive("frames")
        if msg is None:
            continue

        frame = msg["frame"]

        faces = app.get(frame)

        results = []

        for face in faces:
            bbox = face.bbox.astype(int).tolist()

            results.append({
                "bbox": bbox,
                "confidence": float(face.det_score),
                "embedding": face.embedding.tolist()  # 🔥 това е за разпознаване
            })

        bus.send_json("faces", results)