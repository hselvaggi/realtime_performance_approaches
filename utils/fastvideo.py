import cv2
from queue import Queue
from threading import Thread


class FastVideoStream(object):

    def __init__(self, path, queueSize):
        self.stream = cv2.VideoCapture(path)
        self.stopped = False
        self.Q = Queue(maxsize=queueSize)

    def start(self):
        t = Thread(target=self.read_frames, args=())
        t.daemon = True
        t.start()

    def read_frames(self):
        while not self.stopped:
            if not self.Q.full():
                grabbed, frame = self.stream.read()

                if not grabbed:
                    self.stop()
                else:
                    self.Q.put(frame)

    def read(self):
            return self.Q.get()

    def stop(self):
            self.stopped = True


def stream_from_camera(callback):
    cap = FastVideoStream(0, 5)
    cap.start()

    def wrapper():
        result = True
        while result is not None:
            frame = cap.read()
            result = callback(frame)

    return wrapper