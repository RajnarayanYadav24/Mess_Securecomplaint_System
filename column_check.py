from db import get_db_connection

conn = get_db_connection()
cur = conn.cursor()
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = 'mess_complaints';
""")
columns = cur.fetchall()
for col in columns:
    print(col)
cur.close()
conn.close()
