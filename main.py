import multiprocessing as mp

from processes.camera import camera_process
from processes.detection import detection_process
from processes.face import face_process
from processes.brain import brain_process
from processes.retrain import retrain_process

if __name__ == "__main__":
    mp.set_start_method("spawn")

    processes = [
        mp.Process(target=camera_process),
        mp.Process(target=detection_process),
        mp.Process(target=face_process),
        mp.Process(target=brain_process),
        mp.Process(target=retrain_process),
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()