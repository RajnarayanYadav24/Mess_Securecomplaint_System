from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from db import insert_complaint, get_all_complaints,mark_complaint_resolved,delete_complaint


load_dotenv()
WARDEN_USERNAME = os.getenv("WARDEN_USERNAME")
WARDEN_PASSWORD = os.getenv("WARDEN_PASSWORD")

app = Flask(__name__)



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

        insert_complaint(name, room, mobile, branch, complaint)

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
    complaints = get_all_complaints()
    return render_template('dashboard.html', complaints=complaints)

# mark complaint
@app.route('/resolve/<int:complaint_id>')
def mark_resolved(complaint_id):
    mark_complaint_resolved(complaint_id)
    return redirect(url_for('dashboard'))

# delete complaint
@app.route('/delete/<int:complaint_id>')
def delete_complaint_route(complaint_id):
    delete_complaint(complaint_id)
    return redirect(url_for('dashboard'))




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
