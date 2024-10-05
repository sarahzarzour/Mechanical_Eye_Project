# 🦾 Mechanical Eye Project

This project implements a **mechanical eye system** that detects blinks, winks, and gaze direction using a webcam. It leverages facial landmark detection to track the movement of pupils, identify eye activities (blinking, winking), and integrates with servos controlled by an Arduino to simulate these movements in a mechanical eye.

---

## ✨ Features

- **Blink and Wink Detection**: Detects blinks and winks using the Eye Aspect Ratio (EAR) method.
- **Gaze Tracking**: Tracks the user's gaze direction (left, right, or center) based on pupil location.
- **Servo Integration** *(Optional)*: Replicate detected eye movements using servos connected to an Arduino.
- **Pupil Detection**: Identifies and marks pupil position on the video feed in real-time.
- **Facial Landmark Detection**: Uses `dlib` to detect and track eye landmarks for pupil and blink/wink analysis.

---

## 🔧 Requirements

### Python Packages
Install the required Python libraries by running the following command:
```bash
pip install -r requirements.txt
```
### Python Packages
The key libraries used in this project include:
- `opencv-python` (for image processing)
- `dlib` (for facial landmark detection)
- `numpy` (for numerical computations)
- `pyFirmata2` (for Arduino communication, *optional*)

### Hardware (Optional)
- **Arduino**: Used to control servos for eye movement.
- **Servos**: To simulate mechanical eye movements.
- **3D Printed Models**: For physical eye components (STL files provided).

---

## 🚀 Installation

### 1. Clone the Repository
To get started, clone this repository to your local machine:
```bash
git clone https://github.com/yourusername/Mechanical_Eye_Project.git
cd Mechanical_Eye_Project
```
## Install the Dependencies: 
Install the Python libraries as described in the Requirements section.

Download the Shape Predictor File: Download the pre-trained shape_predictor_68_face_landmarks.dat file from here and place it in the project directory.
(https://sourceforge.net/projects/dclib/)

## Connect the Arduino:

- Connect the servos to pins 5, 6, and 7 on your Arduino.
- Connect the Arduino to your computer.
- Uncomment the pyfirmata2 section in the code to enable servo control.
## 🖨️ 3D Printing
The project includes STL files for printing mechanical eyes. These can be found in the models folder.
 Instructions:
- Download the files.
- Use a 3D printer to create the mechanical eye model.
- Assemble the parts and attach the servos to the eye components.
## 🛠️Troubleshooting
- Webcam Issues: If the webcam doesn't start, ensure it's properly connected and recognized by your system.
- Empty Eye Frames: This error occurs if the eyes are not detected. Ensure the camera captures your face clearly and adjust the lighting conditions.
- Arduino Not Detected: If using Arduino, ensure you’ve connected the right port and the servos are wired correctly.

Feel free to contribute to the project by submitting issues or pull requests!




