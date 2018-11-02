import cv2
import sys
from utils.opencvutils import resize, show_fps, display_result
from utils.fastvideo import stream_from_camera
from process_utils import forked_function, cleanup
from utils.functions import detector as detector_


detector = forked_function(detector_)


@stream_from_camera
@resize(640, 480)
@show_fps
@display_result('image')
def show_image(image):
    region = []

    region = detector(image, region)

    for i, d in enumerate(region):
        image = cv2.rectangle(image, (d.left(), d.top()), (d.right(), d.bottom()), (255, 0, 0), 2)

    key = cv2.waitKey(1)
    if key == 27:
        cleanup()
        return None
    return image


if __name__ == '__main__':
    show_image()

