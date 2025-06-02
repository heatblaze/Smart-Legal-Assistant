from flask_sqlalchemy import SQLAlchemy
#from app import db
# Create the SQLAlchemy db instance
db = SQLAlchemy()

# Document model
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    risks = db.Column(db.Text)

# QnA model
class QnA(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=True)
    user_feedback = db.Column(db.String(255))
    rating = db.Column(db.Integer)

class DocumentVersion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('document.id'))
    version_number = db.Column(db.Integer)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

