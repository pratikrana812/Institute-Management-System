# Institute-Management-System
The Institute Management System is a complete software solution designed for schools and coaching institutes to manage their daily operations efficiently. The system includes a Web Application for Admin management and an Android Mobile Application for Students. The Admin Panel allows administrators
# Institute Management System

## Overview

The **Institute Management System** is a web-based software designed for schools and coaching institutes to manage students, fees, and attendance efficiently.

The system consists of:

* **Python Flask Backend API**
* **Admin Web Panel (HTML, CSS, JavaScript)**
* **Student Mobile Web App (Android WebView compatible)**
* **SQLite Database**

This project helps institutes digitize their daily operations such as student management, fee collection, and attendance tracking.

---

# Technology Stack

### Backend

* Python
* Flask API
* SQLite Database
* Flask-CORS

### Frontend

* HTML
* CSS
* JavaScript
* Fetch API

---

# Project Structure

```
project-folder/
│
├── backend/
│   ├── app.py
│   ├── database.db
│   ├── schema.sqlite.sql
│
├── frontend_admin/
│   ├── index.html
│   ├── students.html
│   ├── fees.html
│   ├── attendance.html
│   ├── exams.html
│   ├── css/
│   └── js/
│
├── frontend_mobile/
│   ├── index.html
│   ├── dashboard.html
│   ├── attendance.html
│   ├── fees.html
│   ├── exams.html
│   ├── css/
│   └── js/
│
└── README.md
```

---

# Features

## Admin Panel

* Admin login system
* Add, view and delete students
* Student database management
* Fee structure and payment tracking
* Attendance management
* View student records

## Student Mobile Portal

* Student login
* View attendance records
* View fee status
* View exam information

---

# Database Tables

The system uses SQLite with the following tables:

* **users**
* **students**
* **fees**
* **fee_payments**
* **attendance**

---

# Installation Guide

## 1 Install Python

Make sure Python is installed on your system.

Check version:

```
python --version
```

---

## 2 Install Required Libraries

```
pip install flask flask-cors
```

---

## 3 Run the Backend Server

Navigate to the backend folder:

```
cd backend
```

Run the server:

```
python app.py
```

Server will start on:

```
http://localhost:5000
```

---

# API Endpoints

## Authentication

### Login

```
POST /api/login
```

Request:

```
{
"username":"admin",
"password":"admin123"
}
```

---

## Students

Get all students

```
GET /api/students
```

Get student by ID

```
GET /api/students/{student_id}
```

Add student

```
POST /api/students
```

Delete student

```
DELETE /api/students/{student_id}
```

---

## Fees

Get all fee records

```
GET /api/fees
```

Get student fee

```
GET /api/fees/{student_id}
```

Pay fee

```
POST /api/fees/pay
```

---

## Attendance

Get attendance records

```
GET /api/attendance
```

Get student attendance

```
GET /api/attendance/student/{student_id}
```

Mark attendance

```
POST /api/attendance
```

---

# Running Frontend

Open the admin panel in browser:

```
frontend_admin/index.html
```

For mobile interface open:

```
frontend_mobile/index.html
```

Or run inside an Android WebView application.

---

# Testing APIs

Example CURL command:

```
curl -X GET http://localhost:5000/api/students
```

---

# Future Improvements

* Role based access control
* Online fee payment integration
* SMS notifications
* Parent login portal
* Exam result management
* Android native mobile app

---

# License

This project is open source and can be used for educational and institutional purposes.

---

# Author

Institute Management System Project
