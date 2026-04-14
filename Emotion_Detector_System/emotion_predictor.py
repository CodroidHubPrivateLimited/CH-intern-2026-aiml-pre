import numpy as np

emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]

def get_emotion(prediction):

    max_index = int(np.argmax(prediction))
    emotion = emotion_labels[max_index]

    return emotion