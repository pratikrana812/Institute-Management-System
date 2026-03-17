import os
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from frontends

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'database.db')
SCHEMA_FILE = os.path.join(BASE_DIR, 'schema.sqlite.sql')

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    print(f"Checking database at {DB_FILE}...")
    conn = get_db_connection()
    try:
        # Check if a critical table exists
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'")
        if not cursor.fetchone():
            print(f"Tables missing. Initializing database from {SCHEMA_FILE}...")
            with open(SCHEMA_FILE, 'r') as f:
                conn.executescript(f.read())
            conn.commit()
            print("Database initialized successfully.")
        else:
            print("Database tables already exist.")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

# Initialize immediately
init_db()

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "School Institute Management System API is running."})

# ================= AUTHENTICATION ================= #
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"status": "error", "message": "Username and password required"}), 400
        
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
    
    if user:
        response = {
            "status": "success", 
            "message": "Login successful",
            "user": {
                "id": user['id'],
                "username": user['username'],
                "role": user['role']
            }
        }
        # If student, fetch student details
        if user['role'] == 'student':
            student = conn.execute("SELECT student_id, name, class FROM students WHERE user_id = ?", (user['id'],)).fetchone()
            if student:
                response['user']['student_id'] = student['student_id']
                response['user']['name'] = student['name']
                response['user']['class'] = student['class']
                
        conn.close()
        return jsonify(response)
        
    conn.close()
    return jsonify({"status": "error", "message": "Invalid username or password"}), 401

# ================= STUDENTS API ================= #
@app.route('/api/students', methods=['GET'])
def get_students():
    conn = get_db_connection()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    conn = get_db_connection()
    student = conn.execute("SELECT * FROM students WHERE student_id = ?", (student_id,)).fetchone()
    conn.close()
    if student:
        return jsonify(dict(student))
    return jsonify({"status": "error", "message": "Student not found"}), 404

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.json
    conn = get_db_connection()
    
    # Optional: create user login for this student
    user_id = None
    if data.get('create_login'):
        username = data.get('contact', data.get('name').replace(' ', '').lower())
        password = 'password123' # Default password
        try:
            cursor = conn.execute("INSERT INTO users (username, password, role) VALUES (?, ?, 'student')", (username, password))
            user_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            pass # username exists

    cursor = conn.execute("""
        INSERT INTO students (user_id, name, class, contact, address, admission_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (user_id, data.get('name'), data.get('class'), data.get('contact'), data.get('address'), data.get('admission_date')))
    
    student_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Student added successfully", "student_id": student_id})

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Student deleted successfully"})

# ================= FEES API ================= #
@app.route('/api/fees', methods=['GET'])
def get_fees():
    conn = get_db_connection()
    # Join with students to get names
    fees = conn.execute("""
        SELECT f.*, s.name as student_name, s.class 
        FROM fees f 
        JOIN students s ON f.student_id = s.student_id
    """).fetchall()
    conn.close()
    return jsonify([dict(row) for row in fees])

@app.route('/api/fees/<int:student_id>', methods=['GET'])
def get_student_fees(student_id):
    conn = get_db_connection()
    fees = conn.execute("SELECT * FROM fees WHERE student_id = ?", (student_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in fees])

@app.route('/api/fees/pay', methods=['POST'])
def pay_fee():
    data = request.json
    fee_id = data.get('fee_id')
    amount = float(data.get('amount'))
    
    conn = get_db_connection()
    fee = conn.execute("SELECT * FROM fees WHERE fee_id = ?", (fee_id,)).fetchone()
    if not fee:
        conn.close()
        return jsonify({"status": "error", "message": "Fee record not found"}), 404
        
    new_paid = fee['paid_amount'] + amount
    status = 'paid' if new_paid >= fee['total_amount'] else 'partial'
    date_now = datetime.now().strftime('%Y-%m-%d')
    
    conn.execute("UPDATE fees SET paid_amount = ?, status = ?, last_payment_date = ? WHERE fee_id = ?", 
                 (new_paid, status, date_now, fee_id))
    
    conn.execute("INSERT INTO fee_payments (fee_id, amount_paid) VALUES (?, ?)", (fee_id, amount))
    
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": f"Payment of {amount} recorded successfully"})

# ================= ATTENDANCE API ================= #
@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    date = request.args.get('date')
    class_name = request.args.get('class')
    
    conn = get_db_connection()
    query = """
        SELECT a.*, s.name as student_name, s.class 
        FROM attendance a 
        JOIN students s ON a.student_id = s.student_id
        WHERE 1=1
    """
    params = []
    if date:
        query += " AND a.date = ?"
        params.append(date)
    if class_name:
        query += " AND s.class = ?"
        params.append(class_name)
        
    records = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(row) for row in records])

@app.route('/api/attendance/student/<int:student_id>', methods=['GET'])
def get_student_attendance(student_id):
    conn = get_db_connection()
    records = conn.execute("SELECT * FROM attendance WHERE student_id = ? ORDER BY date DESC", (student_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in records])

@app.route('/api/attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    student_id = data.get('student_id')
    date = data.get('date')
    status = data.get('status')
    
    if not all([student_id, date, status]):
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO attendance (student_id, date, status) 
            VALUES (?, ?, ?) 
            ON CONFLICT(student_id, date) DO UPDATE SET status = excluded.status
        """, (student_id, date, status))
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"status": "error", "message": str(e)}), 500
        
    conn.close()
    return jsonify({"status": "success", "message": "Attendance marked successfully"})

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
