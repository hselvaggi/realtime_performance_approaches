import cv2
import sys
from utils.opencvutils import stream_from_camera, display_result, resize, show_fps
import dlib
import multiprocessing as mp

request = mp.Queue()
response = mp.Queue()
process = None


def detector():
    detector = dlib.get_frontal_face_detector()

    while True:
        image = request.get()
        dets = detector(image, 1)
        response.put(dets)


@stream_from_camera
@resize(640, 480)
@show_fps
@display_result('image')
def show_image(image):
    global process
    region = []
    candidate_region = None

    if request.empty():
        request.put(image)

    if not response.empty():
        candidate_region = response.get_nowait()
        region = candidate_region

    for d in region:
        image = cv2.rectangle(image, (d.left(), d.top()), (d.right(), d.bottom()), (255, 0, 0), 2)

    key = cv2.waitKey(1)
    if key == 27:
        process.terminate()
        sys.exit(0)
    return image


if __name__ == '__main__':
    process = mp.Process(target=detector)
    process.start()
    show_image()

