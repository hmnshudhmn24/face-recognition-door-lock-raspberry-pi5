import cv2
import numpy as np
import face_recognition
import os
import time
import RPi.GPIO as GPIO

# ========== GPIO Setup ==========
RELAY_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

# ========== Load Known Faces ==========
KNOWN_FACES_DIR = "known_faces"
known_face_encodings = []
known_face_names = []

print("[INFO] Loading known faces...")
for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(KNOWN_FACES_DIR, filename)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            name = os.path.splitext(filename)[0]
            known_face_names.append(name)
        else:
            print(f"[WARNING] No face found in {filename}")

# ========== Face Recognition Loop ==========
print("[INFO] Starting camera...")
video_capture = cv2.VideoCapture(0)

process_this_frame = True
UNLOCK_DELAY = 5  # seconds

try:
    while True:
        ret, frame = video_capture.read()
        if not ret:
            continue

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    print(f"[ACCESS GRANTED] Welcome, {name}!")

                    # Unlock door
                    GPIO.output(RELAY_PIN, GPIO.HIGH)
                    print("[DOOR] Unlocked")
                    time.sleep(UNLOCK_DELAY)
                    GPIO.output(RELAY_PIN, GPIO.LOW)
                    print("[DOOR] Locked")
                else:
                    print("[ACCESS DENIED] Unknown person detected")

        process_this_frame = not process_this_frame

        # Display video feed
        for (top, right, bottom, left) in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("Face Recognition Door Lock", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("[INFO] Exiting...")

finally:
    video_capture.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()

