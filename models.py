from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy outside of create_app to be available for models
db = SQLAlchemy()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    # The 'cascade="all, delete-orphan"' ensures comments are deleted with the task.
    comments = db.relationship('Comment', backref='task', lazy=True, cascade="all, delete-orphan")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)