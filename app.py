from flask import Flask, render_template, request, jsonify, send_from_directory
import cv2
import face_recognition
import numpy as np
import base64
import io
from database import init_db, add_user, get_all_encodings, mark_attendance, get_attendance_history
import os

app = Flask(__name__)
KNOWN_FACES_DIR = 'known_faces'

# Initialize DB
init_db()

# Load known face encodings (call this when needed)
def load_known_encodings():
    known_encodings = get_all_encodings()
    return known_encodings

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/view')
def view():
    history = get_attendance_history()
    return render_template('view.html', history=history)

# Endpoint to register a new user (admin uploads image)
@app.route('/api/register_user', methods=['POST'])
def register_user():
    name = request.json['name']
    image_data = request.json['image']  # Base64 image
    image_bytes = base64.b64decode(image_data.split(',')[1])  # Remove data URL prefix
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Detect and encode face
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    if not face_locations:
        return jsonify({'error': 'No face detected'}), 400
    
    face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
    face_encoding_bytes = face_encoding.tobytes()
    
    # Save image to folder (optional, for reference)
    filename = f"{name}.jpg"
    cv2.imwrite(os.path.join(KNOWN_FACES_DIR, filename), image)
    
    user_id = add_user(name, face_encoding_bytes)
    return jsonify({'success': True, 'user_id': user_id})

# Endpoint for attendance marking (processes base64 image from frontend)
@app.route('/api/mark_attendance', methods=['POST'])
def mark_attendance_api():
    image_data = request.json['image']  # Base64 image from webcam
    image_bytes = base64.b64decode(image_data.split(',')[1])
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        return jsonify({'error': 'Invalid image'}), 400
    
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    if not face_locations:
        return jsonify({'error': 'No face detected'}), 400
    
    face_encoding = face_recognition.face_encodings(rgb_image, face_locations)[0]
    
    # Compare with known encodings
    known_encodings = load_known_encodings()
    matches = face_recognition.compare_faces(list(known_encodings.values()), face_encoding)
    names = list(known_encodings.keys())
    
    if True in matches:
        match_index = matches.index(True)
        user_name = names[match_index]
        # Get user_id from DB (simplified; in production, query by name)
        conn = sqlite3.connect('attendance.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM users WHERE name = ?', (user_name,))
        user_id = cursor.fetchone()[0]
        conn.close()
        
        mark_attendance(user_id)
        return jsonify({'success': True, 'name': user_name})
    else:
        return jsonify({'error': 'Unknown face'}), 400

if __name__ == '__main__':
    os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
    app.run(debug=True)