import cv2
import numpy as np
from utils.message_bus import MessageBus


def slam_process():

    bus = MessageBus()

    orb = cv2.ORB_create(2000)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    prev_kp = None
    prev_des = None

    x = 0
    y = 0

    frame_sub = bus.subscribe("frames")

    while True:

        frame = bus.receive_frame(frame_sub)

        if frame is None:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        kp, des = orb.detectAndCompute(gray, None)

        if prev_des is not None and des is not None:

            matches = bf.match(prev_des, des)

            if len(matches) > 10:

                dx = np.random.uniform(-0.05, 0.05)
                dy = np.random.uniform(-0.05, 0.05)

                x += dx
                y += dy

        prev_kp = kp
        prev_des = des

        pose = {
            "x": float(x),
            "y": float(y)
        }

        bus.send_json("robot_pose", pose)