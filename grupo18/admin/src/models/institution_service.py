from datetime import datetime
from src.models.database import db

class Institution_Service(db.Model):
    __tablename__ = "institution_services"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"), nullable=False) #FOREIGN KEY
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False) #FOREIGN KEY
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    service = db.relationship('Service', back_populates='institutions')

    def __init__(self,institution_id,service_id):
        self.institution_id = institution_id
        self.service_id = service_id