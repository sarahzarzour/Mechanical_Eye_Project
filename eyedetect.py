import cv2
import dlib
import numpy as np
# import pyfirmata2

# PORT =  pyfirmata2.Arduino.AUTODETECT
# board = pyfirmata2.Arduino(PORT)
# servo_5 = board.get_pin('d:5:s')
# servo_6 = board.get_pin('d:6:s')
# servo_7 = board.get_pin('d:7:s')



# Load the pre-trained facial landmark detector
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Function to detect and return pupil location
def detect_pupil(eye_frame):
    gray_eye = cv2.cvtColor(eye_frame, cv2.COLOR_BGR2GRAY)
    gray_eye = cv2.equalizeHist(gray_eye)  # Improve contrast for better detection
    blurred_eye = cv2.GaussianBlur(gray_eye, (7, 7), 0)
    _, threshold_eye = cv2.threshold(blurred_eye, 30, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(threshold_eye, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        center = (int(x), int(y))
        return center
    return None

# Function to calculate eye aspect ratio (EAR)
def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# Constants for blink detection
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 3
blink_counter = 0

# Webcam capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame from webcam.")
        break
    
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Get coordinates for left and right eyes
        left_eye = np.array([(landmarks.part(36).x, landmarks.part(36).y),
                             (landmarks.part(37).x, landmarks.part(37).y),
                             (landmarks.part(38).x, landmarks.part(38).y),
                             (landmarks.part(39).x, landmarks.part(39).y),
                             (landmarks.part(40).x, landmarks.part(40).y),
                             (landmarks.part(41).x, landmarks.part(41).y)], np.int32)
        right_eye = np.array([(landmarks.part(42).x, landmarks.part(42).y),
                              (landmarks.part(43).x, landmarks.part(43).y),
                              (landmarks.part(44).x, landmarks.part(44).y),
                              (landmarks.part(45).x, landmarks.part(45).y),
                              (landmarks.part(46).x, landmarks.part(46).y),
                              (landmarks.part(47).x, landmarks.part(47).y)], np.int32)

        # Compute the EAR for both eyes
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        # Eye frames for pupil detection
        try:
            left_eye_frame = frame[landmarks.part(37).y:landmarks.part(41).y, landmarks.part(36).x:landmarks.part(39).x]
            right_eye_frame = frame[landmarks.part(43).y:landmarks.part(47).y, landmarks.part(42).x:landmarks.part(45).x]
            
            # Ensure the eye frames are valid before proceeding
            if left_eye_frame.size > 0 and right_eye_frame.size > 0:
                # Detect pupils
                left_pupil = detect_pupil(left_eye_frame)
                right_pupil = detect_pupil(right_eye_frame)

                # Mark the pupils on the original frame with + sign
                if left_pupil:
                    cv2.drawMarker(frame, (landmarks.part(36).x + left_pupil[0], landmarks.part(37).y + left_pupil[1]),
                                   (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)
                if right_pupil:
                    cv2.drawMarker(frame, (landmarks.part(42).x + right_pupil[0], landmarks.part(43).y + right_pupil[1]),
                                   (0, 0, 255), markerType=cv2.MARKER_CROSS, markerSize=10, thickness=2)

                # Simple gaze detection based on the pupil position within the eye
                if left_pupil and right_pupil:
                    left_pupil_x = landmarks.part(36).x + left_pupil[0]
                    right_pupil_x = landmarks.part(42).x + right_pupil[0]

                    left_eye_width = np.linalg.norm(left_eye[0] - left_eye[3])
                    right_eye_width = np.linalg.norm(right_eye[0] - right_eye[3])

                    if left_pupil_x < landmarks.part(36).x + 0.35 * left_eye_width and right_pupil_x < landmarks.part(42).x + 0.35 * right_eye_width:
                        cv2.putText(frame, "Looking Right", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                        # servo_5.write(0)
                    elif left_pupil_x > landmarks.part(36).x + 0.65 * left_eye_width and right_pupil_x > landmarks.part(42).x + 0.65 * right_eye_width:
                        cv2.putText(frame, "Looking Left", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                        # servo_5.write(60)
                    else:
                        cv2.putText(frame, "Looking Center", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                        # servo_5.write(30)
            else:
                print("Empty eye frames detected.")
        except Exception as e:
            print(f"Error in processing eye frames: {e}")

        # Blink or wink detection
        if left_ear < EAR_THRESHOLD and right_ear >= EAR_THRESHOLD:
            cv2.putText(frame, "Winking Left", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            # servo_6.write(30)
        elif right_ear < EAR_THRESHOLD and left_ear >= EAR_THRESHOLD:
            cv2.putText(frame, "Winking Right", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
            # servo_7.write(30)
        elif left_ear < EAR_THRESHOLD and right_ear < EAR_THRESHOLD:
            blink_counter += 1
            if blink_counter >= CONSEC_FRAMES:
                cv2.putText(frame, "Blinking", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
                # servo_6.write(30)
                # servo_7.write(30)
                
        else:
            blink_counter = 0

    # Show the frame
    cv2.imshow("Frame", frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
