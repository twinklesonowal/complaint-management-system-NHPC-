from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# -----------------------------
# User Table
# -----------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True)

    status = db.Column(db.String(20), default="Active")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"


# -----------------------------
# Service Ticket Table
# -----------------------------
class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id = db.Column(db.Integer, primary_key=True)

    ticket_number = db.Column(db.String(20), unique=True)

    employee_name = db.Column(db.String(100), nullable=False)

    department = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(50), nullable=False)

    problem = db.Column(db.Text, nullable=False)

    priority = db.Column(db.String(20), default="Medium")

    status = db.Column(db.String(20), default="Open")

    assigned_to = db.Column(db.String(100), default="Not Assigned")

    resolution_notes = db.Column(db.Text)

    updated_by = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    closed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Ticket {self.ticket_number}>"
    


# -----------------------------
# Asset Table
# -----------------------------
class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)

    asset_code = db.Column(db.String(100), unique=True)

    asset_name = db.Column(db.String(200), nullable=False)

    category = db.Column(db.String(100))

    brand = db.Column(db.String(100))

    model = db.Column(db.String(100))

    serial_number = db.Column(db.String(100))

    location = db.Column(db.String(150))

    assigned_to = db.Column(db.String(100))

    status = db.Column(
        db.String(30),
        default="Available"
    )

    remarks = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Asset {self.asset_code}>"