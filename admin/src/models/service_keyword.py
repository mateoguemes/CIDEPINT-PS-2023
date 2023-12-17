from datetime import datetime
from src.models.database import db

class Service_Keyword(db.Model):
    __tablename__ = "service_keywords"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False) #FOREIGN KEY
    keyword_id = db.Column(db.Integer, db.ForeignKey("keywords.id"), nullable=False) #FOREIGN KEY
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, service_id, keyword_id):
        self.service_id = service_id
        self.keyword_id = keyword_id