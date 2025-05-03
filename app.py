@app.route('/')
def dashboard():
    monday_warning = check_short_staffed(rota_data['monday'])
    # Default staff_suggestion to avoid undefined error
    staff_suggestion = {}  # Empty dict as fallback
    return render_template('index.html', monday_rota=rota_data['monday'], monday_warning=monday_warning, tuesday_rota=rota_data['tuesday'], stock_alerts=[
        {'text': 'Low coffee beans', 'priority': 'Critical'},
        {'text': 'Order milk soon', 'priority': 'Moderate'}
    ], breaks={
        'Alice': '10:00-10:15',
        'Bob': '11:00-11:15'
    }, sentiment='Positive (80%)', cctvrers={
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
