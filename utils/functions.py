import dlib

det = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')

def detector(image):
    global det
    return det(image, 1)


def face_changer(image):
    global det
    faces = det(image, 1)
    detections = None

    for d in faces:
        points = predictor(image, dlib.rectangle(d.left(), d.top(), d.right(), d.bottom()))
        detections = (faces, points)

    return detections