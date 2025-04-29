import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory storage for rota data (resets on app restart)
rota_data = {
    'monday': ['Alice', 'Bob', 'Charlie'],
    'tuesday': ['Dana', 'Emma']
}

def check_short_staffed(staff_list):
    # Simple rule: if fewer than 3 staff, show a warning
    return "Short-staffed!" if len(staff_list) < 3 else None

@app.route('/')
def dashboard():
    monday_warning = check_short_staffed(rota_data['monday'])
    return render_template('index.html',
        monday_rota=rota_data['monday'],
        monday_warning=monday_warning,
        tuesday_rota=rota_data['tuesday'],
        stock_alerts=[
            {'text': 'Low coffee beans', 'priority': 'Critical'},
            {'text': 'Order milk soon', 'priority': 'Moderate'}
        ],
        breaks={'Alice': '10:00-10:15', 'Bob': '11:00-11:15'},
        sentiment='Positive (80%)',
        cctv_metrics={'retention': '7 days', 'anonymized': 'Yes', 'compliance': 'GDPR'},
        hygiene={'last_inspection': 'April 10, 2025', 'rating': '5/5'},
        licensing={'alcohol': 'Dec 2025', 'entertainment': 'Nov 2025'},
        iot={'fridge_temp': '4°C', 'bottles': '50'}
    )

@app.route('/update-rota/<day>', methods=['POST'])
def update_rota(day):
    if day not in ['monday', 'tuesday']:
        return "Invalid day", 400
    # Get the new rota from the form
    new_rota = request.form.get('rota', '')
    # Split the input into a list, strip whitespace, and filter out empty entries
    staff_list = [name.strip() for name in new_rota.split(',') if name.strip()]
    rota_data[day] = staff_list
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# In app.py, add after existing imports and routes (around line 50)
from datetime import datetime

# Mock data for staff availability, sales, and events
staff_availability = {"Alice": ["Monday", "Tuesday"], "Bob": ["Monday"], "Charlie": ["Tuesday"]}
sales_data = {"Monday": "high", "Tuesday": "low"}  # Mock sales: high = need more staff
local_events = {"Monday": "Festival", "Tuesday": "None"}  # Mock events

@app.route('/suggest-staff/<day>')
def suggest_staff(day):
    # Get available staff for the day
    available_staff = [name for name, days in staff_availability.items() if day in days]
    
    # Suggest more staff if sales are high or there's an event
    suggestion = available_staff[:2] if sales_data.get(day) == "high" or local_events.get(day) != "None" else available_staff[:1]
    
    if not suggestion:
        suggestion = ["No staff available"]
    
    return render_template('index.html', 
                         monday_rota=monday_rota,  # Existing data
                         tuesday_rota=tuesday_rota,
                         stock_alerts=stock_alerts,
                         breaks=breaks,
                         sentiment="Positive",  # Mock for CrowdEcho
                         cctv_metrics={"retention": "30 days", "anonymized": "Yes", "compliance": "GDPR"},
                         hygiene={"last_inspection": "2025-04-01", "rating": "5"},
                         licensing={"alcohol": "2025-12-31", "entertainment": "2025-12-31"},
                         iot={"fridge_temp": "4°C", "bottles": "50"},
                         staff_suggestion={day: suggestion})  # New data
