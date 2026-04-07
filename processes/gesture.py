from utils.message_bus import MessageBus


def gesture_process():

    bus = MessageBus()

    pose_sub = bus.subscribe("pose")

    while True:

        pose = bus.receive_json(pose_sub)

        if pose is None:
            continue

        gesture = None

        if len(pose) > 0:

            left_wrist = pose[15]
            right_wrist = pose[16]
            nose = pose[0]

            if left_wrist["y"] < nose["y"] or right_wrist["y"] < nose["y"]:
                gesture = "wave"

        if gesture:

            bus.send_json("gesture", {
                "gesture": gesture
            })