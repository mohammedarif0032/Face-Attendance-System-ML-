⚡ ML Face Attendance System (Python/OpenCV)

A simple, real-time application using Python and Machine Learning (face_recognition) to track attendance via a webcam.

✨ Core Features

Live Recognition: Identifies individuals via webcam.

Deep Learning: Converts faces to 128D encodings for high accuracy.

Auto-Logging: Saves attendance (Name, Date, Time) to AttendanceLog.csv.

Offline: Runs completely locally without internet (after initial setup).

🛠️ Quick Setup (Get Running in 3 Steps)

1. Install Libraries

Run this command in your terminal:  (pip install opencv-python face-recognition numpy pandas)

2. Prepare Data

Create a folder named Faces next to attendance_system.py.

Place clear, frontal images inside. The filename becomes the name on the log.

Filename Example     Log Name

Jane_Doe.jpg         JANE DOE

3. Run the System

Execute the script:

python attendance_system.py

Look into the camera. A green box means attendance is marked.

Press q to close the window.

📂 Output

Check the generated AttendanceLog.csv file for the records.

Name            Date            Time
ALICE SMITH   2025-10-28     14:30:05









