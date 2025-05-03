import os
from flask import Flask, render_template, request, redirect, url_for, Response
from datetime import datetime
import cv2  # OpenCV for video streaming (using opencv-python-headless)

app = Flask(__name__)

# Path to Haar Cascade for person detection (included with OpenCV)
cascade_path = cv2.data.haarcascades + "haarcascade_fullbody.xml"
person_cascade = cv2.CascadeClassifier(cascade_path)

# Global variable to store people count (temporary solution)
global_people_count = 0

# In-memory storage for rota data (resets on app restart)
rota_data = {
    'monday': ['Alice', 'Bob', 'Charlie'],
    'tuesday': ['Dana', 'Emma']
}

def check_short_staffed(staff_list):
    return "Short-staffed!" if len(staff_list) < 3 else None

@app.route('/')
def dashboard():
    monday_warning = check_short_staffed(rota_data['monday'])
    staff_suggestion = {}
    return render_template('index.html', monday_rota=rota_data['monday'], monday_warning=monday_warning, tuesday_rota=rota_data['tuesday'], stock_alerts=[
        {'text': 'Low coffee beans', 'priority': 'Critical'},
        {'text': 'Order milk soon', 'priority': 'Moderate'}
    ], breaks={
        'Alice': '10:00-10:15',
        'Bob': '11:00-11:15'
    }, sentiment='Positive (80%)', cctv_metrics={
        'retention': '7 days',
        'anonymized': 'Yes',
        'compliance': 'GDPR'
    }, hygiene={
        'last_inspection': 'April 10, 2025',
        'rating': '5/5'
    }, licensing={
        'alcohol': 'Dec 2025',
        'entertainment': 'Nov 2025'
    }, iot={
        'fridge_temp': '4°C',
        'bottles': '50'
    }, staff_suggestion=staff_suggestion)

@app.route('/update-rota/<day>', methods=['POST'])
def update_rota(day):
    if day not in ['monday', 'tuesday']:
        return "Invalid day", 400
    new_rota = request.form.get('rota', '')
    staff_list = [name.strip() for name in new_rota.split(',') if name.strip()]
    rota_data[day] = staff_list
    return redirect(url_for('dashboard'))

# Mock data for staff availability, sales, and events
staff_availability = {"Alice": ["Monday", "Tuesday"], "Bob": ["Monday"], "Charlie": ["Tuesday"]}
sales_data = {"Monday": "high", "Tuesday": "low"}
local_events = {"Monday": "Festival", "Tuesday": "None"}

@app.route('/suggest-staff/<day>')
def suggest_staff(day):
    available_staff = [name for name, days in staff_availability.items() if day.capitalize() in days]
    suggestion = available_staff[:2] if sales_data.get(day.capitalize()) == "high" or local_events.get(day.capitalize()) != "None" else available_staff[:1]
    if not suggestion:
        suggestion = ["No staff available"]
    return render_template('index.html', monday_rota=rota_data['monday'], tuesday_rota=rota_data['tuesday'], stock_alerts=[
        {'text': 'Low coffee beans', 'priority': 'Critical'},
        {'text': 'Order milk soon', 'priority': 'Moderate'}
    ], breaks={
        'Alice': '10:00-10:15',
        'Bob': '11:00-11:15'
    }, sentiment="Positive", cctv_metrics={
        "retention": "30 days",
        "anonymized": "Yes",
        "compliance": "GDPR"
    }, hygiene={
        "last_inspection": "2025-04-01",
        "rating": "5"
    }, licensing={
        "alcohol": "2025-12-31",
        "entertainment": "2025-12-31"
    }, iot={
        "fridge_temp": "4°C",
        "bottles": "50"
    }, staff_suggestion={day.capitalize(): suggestion})

# Dahua CCTV streaming route
def generate_frames():
    # Replace with actual Dahua camera credentials and IP
    DAHUA_USERNAME = "admin"
    DAHUA_PASSWORD = "admin"
    DAHUA_IP = "192.168.1.108"  # Example IP, replace with actual
    rtsp_url = f"rtsp://{DAHUA_USERNAME}:{DAHUA_PASSWORD}@{DAHUA_IP}/cam/realmonitor?channel=1&subtype=0"

    # Open the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Could not open RTSP stream")
        return

    # Overcrowding threshold
    OVERCROWDING_THRESHOLD = 10
    overcrowding_status = "Safe"

    while True:
        success, frame = cap.read()
        if not success:
            break

        # Convert frame to grayscale for person detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect people in the frame
        people = person_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 60))
        people_count = len(people)

        # Update global people count
        global global_people_count
        global_people_count = people_count

        # Update overcrowding status
        overcrowding_status = "Overcrowded" if people_count > OVERCROWDING_THRESHOLD else "Safe"

        # Draw rectangles around detected people (optional, for debugging)
        for (x, y, w, h) in people:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Encode the frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        # Yield the frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/crowdecho')
def crowdecho():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/crowdecho_status')
def crowdecho_status():
    global global_people_count
    OVERCROWDING_THRESHOLD = 10
    status = "Overcrowded" if global_people_count > OVERCROWDING_THRESHOLD else "Safe"
    return {"people_count": global_people_count, "status": status}

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
