import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DB_HOST=os.getenv("DB_HOST")
DB_NAME=os.getenv("DB_NAME")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_PORT=os.getenv("DB_PORT")

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def insert_complaint(name, room, mobile, branch, complaint):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO mess_complaints (name, room, mobile, branch, complaint, date_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, room, mobile, branch, complaint, datetime.now()))
    conn.commit()
    cur.close()
    conn.close()

def get_all_complaints():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, name, room, mobile, branch, complaint, date_time, status, action
        FROM mess_complaints
        ORDER BY date_time DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# for marked as Resolved
def mark_complaint_resolved(complaint_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE mess_complaints
        SET status = 'Resolved'
        WHERE id = %s
    """, (complaint_id,))
    conn.commit()
    cur.close()
    conn.close()


# for deletion
def delete_complaint(complaint_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM mess_complaints WHERE id = %s", (complaint_id,))
    conn.commit()
    cur.close()
    conn.close()



