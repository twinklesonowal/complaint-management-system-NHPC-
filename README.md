# 🖥️ NHPC IT Service Desk & Complaint Management System

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.3-black?logo=flask)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange?logo=mysql)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap-7952B3?logo=bootstrap)
![License](https://img.shields.io/badge/License-Educational-green)

A web-based **Complaint & Asset Management System** developed for the **IT Department of NHPC (National Hydroelectric Power Corporation)** during internship training.

The system enables employees to raise IT-related complaints, allows IT staff to manage and resolve them efficiently, and provides managers with centralized control over users, complaints, and IT assets.

---

# 📌 Features

## 👤 Employee

- Secure Login
- Raise New Complaint
- View Complaint Status
- Track Complaint History

---

## 💻 IT Staff

- View Assigned Complaints
- Update Complaint Status
- Assign Technician
- Add Resolution Notes
- Close Complaints

---

## 👨‍💼 IT Manager

- Dashboard with Complaint Statistics
- User Management
- Asset Management
- Complaint Monitoring
- View Asset Details
- Import Asset Inventory from Excel

---

## 📦 Asset Management

- Import Assets from Excel
- Search Assets
- View Asset Details
- Track Asset Status
- Assigned User Information

---

# 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend Programming |
| Flask | Web Framework |
| MySQL | Database |
| SQLAlchemy | ORM |
| HTML5 | Frontend |
| Bootstrap 5 | UI Design |
| Jinja2 | Template Engine |
| Pandas | Excel Import |
| OpenPyXL | Excel Processing |

---

# 📂 Project Structure

```text
Complaint-Management-System/
│
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── images/
│   │   └── js/
│   │
│   ├── templates/
│   │   ├── layouts/
│   │   ├── login.html
│   │   ├── manager_dashboard.html
│   │   ├── employee_dashboard.html
│   │   ├── it_dashboard.html
│   │   ├── manage_users.html
│   │   ├── manage_assets.html
│   │   ├── ticket_details.html
│   │   └── ...
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   └── routes.py
│
├── docs/
│
├── excel/
│
├── requirements.txt
├── run.py
└── README.md
```

---

# 🗄️ Database

The project uses **MySQL**.

Main tables include:

- Users
- Service Tickets
- Assets

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/twinklesonowal/complaint-management-system-NHPC-.git
```

---

## 2. Open Project

```bash
cd complaint-management-system-NHPC-
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Configure Database

Update the database connection inside

```
app/config.py
```

Example

```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@localhost/complaint_system"
```

---

## 7. Create Database

Create a MySQL database named

```
complaint_system
```

---

## 8. Run the Application

```bash
python run.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

## Login Page

> *(Add screenshot here)*

---

## Employee Dashboard

> *(Add screenshot here)*

---

## IT Staff Dashboard

> *(Add screenshot here)*

---

## Manager Dashboard

> *(Add screenshot here)*

---

## Asset Management

> *(Add screenshot here)*

---

## Complaint Details

> *(Add screenshot here)*

---

# 🔒 User Roles

| Role | Permissions |
|------|-------------|
| Employee | Raise and Track Complaints |
| IT Staff | Resolve Complaints |
| IT Manager | Manage Users, Complaints and Assets |

---

# ✨ Key Functionalities

- Role-Based Authentication
- Complaint Lifecycle Management
- Asset Inventory Management
- Dashboard Statistics
- Excel Asset Import
- Search Functionality
- Bootstrap Responsive UI
- Flash Notifications
- Session Management

---

# 📈 Future Enhancements

- Email Notifications
- Asset QR Code Generation
- Complaint Analytics Dashboard
- PDF Report Generation
- Complaint Priority Prediction
- Role-Based Permission Module
- Audit Logs
- REST API Integration

---

# 👩‍💻 Developed By

**Twinkle Sonowal**

Bachelor of Computer Applications (BCA)

Internship Project

National Hydroelectric Power Corporation (NHPC)

---

# 📄 License

This project is developed for **educational and internship purposes**.

© 2026 Twinkle Sonowal
