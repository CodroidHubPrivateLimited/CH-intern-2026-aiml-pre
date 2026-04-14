from tensorflow.keras.models import load_model

class EmotionModel:

    def __init__(self):
        self.model = load_model("models/emotion_model.hdf5")

    def predict(self, face):

        prediction = self.model.predict(face)

        return prediction