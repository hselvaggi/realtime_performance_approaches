import cv2
from timeit import default_timer as timeit


def resize(max_width, max_height):

    def decorator(callback):
        imh, imw = None, None

        def wrapper(image):
            nonlocal imh, imw
            if imh is None:
                height, width, _ = image.shape
                factor = min(max_height / height, max_width / width)
                imh = int(factor * height)
                imw = int(factor * width)

            image = cv2.resize(image, (imw, imh))
            return callback(image)
        return wrapper

    return decorator


def display_result(name):
    def decorator(callback):
        def wrapper(*args, **wargs):
            image = callback(*args, **wargs)
            if image is not None:
                cv2.imshow(name, image)
            return image
        return wrapper
    return decorator


def show_fps(callback):
    counter = 0
    start_time = 0
    fps = 0

    def wrapper(image):
        nonlocal counter, start_time, fps

        if counter == 10:
            end_time = timeit()
            elapsed = end_time - start_time
            start_time = end_time
            counter = 0

            fps = (10.0 / elapsed)
        elif counter == 0:
            start_time = timeit()

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, 'FPS %.2f' % fps, (10, 30), font, 1, (100, 100, 100))

        counter = counter + 1

        return callback(image)

    return wrapper


def stream_from_camera(callback):
    def wrapper():
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if ret:
                callback(frame)

    return wrapper


def resize_image(image, max_width, max_height):
    height, width, _ = image.shape
    factor = min(max_height / height, max_width / width)
    imh = int(factor * height)
    imw = int(factor * width)
    image = cv2.resize(image, (imw, imh))

    return image


