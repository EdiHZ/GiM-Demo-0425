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
