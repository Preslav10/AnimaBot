import multiprocessing as mp

from processes.camera import camera_process
from processes.detection import detection_process
from processes.tracking import tracking_process
from processes.pose import pose_process
from processes.face import face_process
from processes.scene_memory import scene_memory_process
from processes.brain import brain_process
from processes.retrain import retrain_process
from processes.slam import slam_process
from processes.gesture import gesture_process
from processes.vision_brain import vision_brain_process

if __name__ == "__main__":

    mp.set_start_method("spawn")

    processes = [

        mp.Process(target=camera_process),

        mp.Process(target=detection_process),

        mp.Process(target=tracking_process),

        mp.Process(target=pose_process),

        mp.Process(target=face_process),

        mp.Process(target=scene_memory_process),

        mp.Process(target=brain_process),

        mp.Process(target=retrain_process),

        mp.Process(target=slam_process),

        mp.Process(target=gesture_process),
        
        mp.Process(target=vision_brain_process),
    ]

    for p in processes:
        p.start()

    for p in processes:
        p.join()