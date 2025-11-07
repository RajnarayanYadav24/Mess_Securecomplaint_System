from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime
from dotenv import load_dotenv
from db import insert_complaint, get_all_complaints,mark_complaint_resolved,delete_complaint,get_db_connection,verify_student_login
from send_email import send_email


load_dotenv()
WARDEN_USERNAME = os.getenv("WARDEN_USERNAME")
WARDEN_PASSWORD = os.getenv("WARDEN_PASSWORD")
Student1_name = os.getenv("Student1_name")
Student1_password = os.getenv("Student1_password")
app = Flask(__name__)



@app.route('/')
def landing():
    return render_template('landing.html')


# Student Login
@app.route('/stulogin', methods=['GET','POST'])
def student_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        student = verify_student_login(username, password)
        if student:
            return redirect(url_for('student'))
        else:
            return "<h3 style='color:red;'>Invalid credentials. Try again.</h3>"
        
    return render_template('student_login.html')    

# Student complaint form
@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        name = request.form.get('name')
        room = request.form.get('room')
        mobile = request.form.get('mobile')
        email = request.form.get('email')
        branch = request.form.get('branch')
        complaint = request.form.get('complaint')

        insert_complaint(name, room, mobile, email, branch, complaint)

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
     # 1. Mark complaint as resolved in DB
    mark_complaint_resolved(complaint_id)

    # 2. Get student email for that complaint
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT email, name FROM MESS_Complaints WHERE id = %s", (complaint_id,))
    result = cur.fetchone()
    conn.close()

    if result:
        student_email, student_name = result

        # 3. Send an email notification
        subject = "Notification: Your Mess Complaint Has Been Resolved"

        body = f"""
        Dear {student_name},

        This is to inform you that your mess complaint (Complaint ID: {complaint_id}) has been successfully resolved.

        Thank you for your patience and cooperation during the resolution process.  
        If you have any further concerns or notice any related issues, please feel free to contact the hostel office.

        Warm regards,  
        Warden Sir Name  
        Warden, Aryabhatta Hostel  
        Harcourt Butler Technical University, Kanpur

        """

        try:
            send_email(student_email, subject, body)
        except Exception as e:
            print(f"Error sending email: {e}")

    # 4. Redirect back to dashboard
    return redirect(url_for('dashboard'))

# delete complaint
@app.route('/delete/<int:complaint_id>')
def delete_complaint_route(complaint_id):
    delete_complaint(complaint_id)
    return redirect(url_for('dashboard'))




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
