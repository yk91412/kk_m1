from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task():
    status = db.Column(db.String(5),nullable=False)
    title = db.Column(db.text, nullable=False)
    ap_num = db.Column(db.Integer, primary_key=True)
    application_date = db.Column(db.Date, nullable=False)
    applicant= db.Column(db.String(50), nullable=False)
    summary = db.Column(db.text,nullable=False)