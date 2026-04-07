from deep_sort_realtime.deepsort_tracker import DeepSort
from utils.message_bus import MessageBus


def tracking_process():

    bus = MessageBus()

    tracker = DeepSort(max_age=30)

    det_sub = bus.subscribe("detections")
    frame_sub = bus.subscribe("frames")

    while True:

        detections = bus.receive_json(det_sub)
        frame = bus.receive_frame(frame_sub)

        if detections is None or frame is None:
            continue

        dets = []

        for d in detections:

            bbox = d["bbox"]
            conf = d["confidence"]
            label = d["label"]

            dets.append((bbox, conf, label))

        tracks = tracker.update_tracks(dets, frame=frame)

        objects = []

        for t in tracks:

            if not t.is_confirmed():
                continue

            objects.append({
                "id": t.track_id,
                "bbox": t.to_ltrb(),
                "label": t.get_det_class()
            })

        bus.send_json("tracked_objects", objects)