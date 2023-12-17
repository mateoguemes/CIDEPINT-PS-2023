from datetime import datetime
from src.models.database import db

class User_Institution(db.Model):
    __tablename__ = "user_institutions"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) #FOREIGN KEY
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"), nullable=False) #FOREIGN KEY
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,user_id,institution_id):
        self.user_id=user_id
        self.institution_id=institution_id

    def get_institution_id(user_id: int)-> int:
        """
        Returns the id of an institution of the user given its id
        """
        institution_id = User_Institution.query.filter_by(user_id=user_id).first()
        return institution_id.institution_id if institution_id != None else None