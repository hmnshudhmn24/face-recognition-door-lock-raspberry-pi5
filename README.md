
# 🔒 Face Recognition Door Lock – Raspberry Pi

Welcome to the **Face Recognition Door Lock** project, a smart security system using a Raspberry Pi and face recognition technology to automate and secure access through doors! 🚪📸

## 🧠 What It Does
This project captures a live image of a person standing at the door using the Raspberry Pi Camera and compares it with stored facial data. If a match is found, the system unlocks the door. Otherwise, it denies access and can optionally alert the owner.

## 💡 Features
- 🧍 Face detection and recognition using OpenCV
- 🔓 Unlocks door via GPIO control on successful face match
- 💾 Local database of known faces
- 🛑 Logs access attempts with timestamps and result (Access Granted/Denied)
- 📨 Optional email alerts for unknown access attempts

## 🛠️ Hardware Required
- Raspberry Pi (4/3B+ recommended)
- Raspberry Pi Camera Module or USB Webcam
- Relay module (for door lock control)
- Jumper wires, breadboard
- Power supply

## 📦 Installation

```bash
sudo apt-get update
sudo apt-get install python3-opencv python3-pip
pip3 install face_recognition numpy imutils
```

## 🧑‍💻 Usage

```bash
python3 face_recognition_lock.py
```

Make sure your known faces are placed in a `known_faces/` directory.

## 📂 Project Structure

```
face-recognition-door-lock-raspberry-pi/
├── face_recognition_lock.py
├── known_faces/
│   ├── person1.jpg
│   └── person2.jpg
├── logs/
│   └── access_log.txt
└── README.md
```

## 📈 Future Enhancements
- Add voice response using `espeak` or `pyttsx3`
- Implement cloud backup for face database
- Add web-based UI for access logs

## 🤖 Powered By
- Python
- OpenCV
- face_recognition (dlib)
- Raspberry Pi GPIO
