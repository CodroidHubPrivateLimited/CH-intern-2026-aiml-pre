import cv2

class Camera:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):

        ret, frame = self.cap.read()

        if ret:
            return frame

        return None