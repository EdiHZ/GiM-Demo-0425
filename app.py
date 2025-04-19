from flask import Flask, render_template

app = Flask(__name__)

# Sample data for the demo
staff_list = ["Alice", "Bob", "Charlie"]
availability = {"Alice": ["Monday", "Tuesday"], "Bob": ["Monday", "Wednesday"], "Charlie": ["Tuesday"]}
skill_levels = {"Alice": 2, "Bob": 1, "Charlie": 1}
staff_needed = 5

# Monday Rota
monday_rota = [staff for staff in sorted(staff_list, key=lambda x: skill_levels[x], reverse=True) 
               if "Monday" in availability[staff]][:staff_needed]
monday_warning = f"Warning: Only {len(monday_rota)} staff assigned, need {staff_needed}" if len(monday_rota) < staff_needed else ""

# Tuesday Rota
tuesday_rota = [staff for staff in sorted(staff_list, key=lambda x: skill_levels[x], reverse=True) 
                if "Tuesday" in availability[staff]][:staff_needed]
tuesday_warning = f"Warning: Only {len(tuesday_rota)} staff assigned, need {staff_needed}" if len(tuesday_rota) < staff_needed else ""

# Stock Alerts
stock_list = {"Milk": 5, "Coffee": 20}
thresholds = {"Milk": 10, "Coffee": 5}
stock_alerts = []
for item in stock_list:
    if stock_list[item] < thresholds[item]:
        restock_amount = thresholds[item] * 2
        priority = "Critical" if stock_list[item] <= thresholds[item] * 0.5 else "Moderate"
        stock_alerts.append({"text": f"{item} is low! Current: {stock_list[item]} - Restock to: {restock_amount}", 
                            "priority": priority})

# Break Schedule
shift_lengths = {"Alice": 8, "Bob": 6, "Charlie": 4}
break_preferences = {"Alice": 2, "Bob": 3, "Charlie": 2}
breaks = {staff: f"15-min break after {break_preferences[staff]} hours" if shift_lengths[staff] >= 6 else "No break needed" 
          for staff in shift_lengths}

@app.route('/')
def dashboard():
    return render_template('dashboard.html', 
                          monday_rota=monday_rota, monday_warning=monday_warning,
                          tuesday_rota=tuesday_rota, tuesday_warning=tuesday_warning,
                          stock_alerts=stock_alerts, breaks=breaks)

if __name__ == '__main__':
    app.run(debug=True)
