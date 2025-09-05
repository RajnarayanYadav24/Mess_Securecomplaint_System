from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
WARDEN_USERNAME = os.getenv("WARDEN_USERNAME")
WARDEN_PASSWORD = os.getenv("WARDEN_PASSWORD")

app = Flask(__name__)

# Ensure CSV exists
if not os.path.exists('complaints.csv'):
    with open('complaints.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Room", "Mobile", "Branch", "Complaint","Date & Time", "Status"])
        #  "Status", "Raised Date" it would be done later


@app.route('/')
def landing():
    return render_template('landing.html')

# Student complaint form
@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        name = request.form.get('name')
        room = request.form.get('room')
        mobile = request.form.get('mobile')
        branch = request.form.get('branch')
        complaint = request.form.get('complaint')

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Pending"  # Default status

        with open('complaints.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, room, mobile, branch, complaint, date, status])

        return render_template('thank_you.html')

    return render_template('feedback_form.html')

# Warden login
@app.route('/warden', methods=['GET', 'POST'])
def warden_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == WARDEN_USERNAME and password == WARDEN_PASSWORD:
            return redirect(url_for('dashboard'))
        else:
            return "<h3 style='color:red;'>Invalid credentials. Try again.</h3>"

    return render_template('warden_login.html')

# Warden dashboard
@app.route('/dashboard')
def dashboard():
    with open('complaints.csv', 'r') as file:
        reader = csv.reader(file)
        data = list(reader)
    return render_template('dashboard.html', complaints=data[1:], headers=data[0])

# mark complaint
@app.route('/resolve/<int:index>')
def mark_resolved(index):
    # Read all complaints
    with open('complaints.csv', 'r') as file:
        reader = list(csv.reader(file))
    
    # Skip header
    header = reader[0]
    data = reader[1:]
    
    # Update status of selected complaint
    data[index][6] = "Resolved"
    
    # Write back to CSV
    with open('complaints.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data)
    
    return redirect(url_for('dashboard'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
