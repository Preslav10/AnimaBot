import mediapipe as mp
from utils.message_bus import MessageBus


def pose_process():

    bus = MessageBus()

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    frame_sub = bus.subscribe("frames")

    while True:

        frame = bus.receive_frame(frame_sub)

        if frame is None:
            continue

        results = pose.process(frame)

        if not results.pose_landmarks:
            continue

        landmarks = []

        for l in results.pose_landmarks.landmark:

            landmarks.append({
                "x": l.x,
                "y": l.y,
                "z": l.z
            })

        bus.send_json("pose", landmarks)