from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html',
        monday_rota=['Alice', 'Bob', 'Charlie'],
        monday_warning='Short-staffed!',
        tuesday_rota=['Dana', 'Emma'],
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

if __name__ == '__main__':
    app.run(debug=True)
