import cv2
import sys
from utils.opencvutils import stream_from_camera, display_result, resize, show_fps
import dlib

detector = dlib.get_frontal_face_detector()


@stream_from_camera
@resize(640, 480)
@show_fps
@display_result('image')
def show_image(image):
    global classifier

    dets = detector(image, 1)

    for i, d in enumerate(dets):
        image = cv2.rectangle(image, (d.left(), d.top()), (d.right(), d.bottom()), (255, 0, 0), 2)

    key = cv2.waitKey(1)
    if key == 27:
        sys.exit(0)
    return image


if __name__ == '__main__':
    show_image()