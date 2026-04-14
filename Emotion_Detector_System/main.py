import cv2
import numpy as np

from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout

from camera import Camera
from emotion_model import EmotionModel
from emotion_predictor import get_emotion
from utils.face_detector import FaceDetector
from utils.preprocess import preprocess_face


class EmotionApp(App):

    def build(self):

        self.camera = Camera()
        self.model = EmotionModel()
        self.detector = FaceDetector()

        self.img = Image()

        layout = BoxLayout()
        layout.add_widget(self.img)

        Clock.schedule_interval(self.update, 1.0 / 30.0)

        return layout

    def update(self, dt):

        frame = self.camera.get_frame()

        if frame is None:
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.detector.detect_faces(rgb_frame)

        if results.detections:

            for detection in results.detections:

                bbox = detection.location_data.relative_bounding_box

                h, w, _ = frame.shape

                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                face = frame[y:y+height, x:x+width]

                if face.size == 0:
                    continue

                face_input = preprocess_face(face)

                prediction = self.model.predict(face_input)

                emotion = get_emotion(prediction)

                cv2.rectangle(frame, (x,y), (x+width,y+height),(0,255,0),2)

                cv2.putText(
                    frame,
                    emotion,
                    (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0,255,0),
                    2
                )

        buf = cv2.flip(frame, 0).tobytes()

        texture = Texture.create(
            size=(frame.shape[1], frame.shape[0]),
            colorfmt='bgr'
        )

        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.img.texture = texture


if __name__ == "__main__":
    EmotionApp().run()