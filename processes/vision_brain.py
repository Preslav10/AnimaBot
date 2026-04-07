from utils.message_bus import MessageBus


def vision_brain_process():

    bus = MessageBus()

    objects_sub = bus.subscribe("tracked_objects")
    pose_sub = bus.subscribe("pose")

    previous_people = set()

    while True:

        objects = bus.receive_json(objects_sub)
        pose = bus.receive_json(pose_sub)

        if objects is None:
            continue

        events = []

        persons = []

        for obj in objects:

            if obj["label"] == "person":
                persons.append(obj["id"])

        current_people = set(persons)

        if len(current_people) > len(previous_people):
            events.append("someone_entered_room")

        previous_people = current_people

        for obj in objects:

            if obj["label"] == "cup":

                for p in persons:

                    events.append("person_holding_cup")

        if pose:

            hip = pose[24]
            shoulder = pose[12]

            if hip["y"] < shoulder["y"]:
                events.append("person_fell")

        if events:

            bus.send_json("vision_events", {
                "events": events
            })