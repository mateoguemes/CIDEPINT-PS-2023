from datetime import datetime
from src.models.database import db

class Institution_Keyword(db.Model):
    __tablename__ = "institution_keywords"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"), nullable=False) #FOREIGN KEY
    keyword_id = db.Column(db.Integer, db.ForeignKey("keywords.id"), nullable=False) #FOREIGN KEY
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,insitution_id,keyword_id):
        self.institution_id = insitution_id
        self.keyword_id = keyword_id
        db.session.add(self)
        db.session.commit()