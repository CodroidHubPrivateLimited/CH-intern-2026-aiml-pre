# GhostPen-AI

### Gesture-Based Air Writing System using Computer Vision

GhostPen-AI is a real-time gesture-controlled writing system that enables users to write, draw, and erase in the air using hand movements. The system leverages computer vision techniques to eliminate the need for physical input devices, creating a touchless and intuitive interaction experience.

---

## Overview

This project uses a webcam to capture hand movements and applies hand-tracking algorithms to detect finger positions. Based on predefined gestures, the system switches between writing, erasing, and selection modes. The output is rendered on a virtual canvas in real time.

---

## Key Features

* Real-time air writing using index finger tracking
* Gesture-based mode switching (Write, Erase, Selection)
* Interactive color selection and canvas controls
* Smooth drawing using motion filtering
* Save drawings as image files
* On-screen mode indication for user feedback

---

## Technology Stack

* Python
* OpenCV
* MediaPipe
* NumPy

---

## Gesture Controls

| Gesture                     | Function       |
| --------------------------- | -------------- |
| Index finger up             | Writing mode   |
| Index and middle finger up  | Selection mode |
| No fingers up (closed hand) | Erase mode     |

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/GhostPen-AI.git
cd GhostPen-AI
```

### Install dependencies

```bash
pip install opencv-python mediapipe numpy
```

### Run the application

```bash
python main.py
```

---

## Project Structure

```
GhostPen-AI/
│── main.py
│── README.md
│── outputs/
```

---

## Applications

* Smart classroom systems
* Touchless user interfaces
* Virtual whiteboards
* Human-computer interaction research

---

## Future Scope

* Handwriting to text conversion using OCR
* Export notes as PDF documents
* Integration with GUI frameworks (Kivy/Tkinter)
* Improved gesture recognition using machine learning models

---


## License

This project is intended for academic and educational use.
