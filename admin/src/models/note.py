from datetime import datetime
from src.models.database import db
from src.models.state import State
from src.models.requirement import Requirement

class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    text = db.Column(db.String(255), nullable=False)
    requirement_id = db.Column(db.Integer, db.ForeignKey("requirements.id"), nullable=False) 
    from_laboratory = db.Column(db.Boolean, nullable=False, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    state = db.relationship('Requirement', backref='requirement_states', foreign_keys=[requirement_id])

    @classmethod
    def add_note(cls, data: dict)->None:
        """
        Adds a note to the database given a form.
        """
        new_note = Note(
            text = data['text'],
            requirement_id = data['requirement_id'],
            from_laboratory = True if 'from_laboratory' in data else False,
            inserted_at = datetime.utcnow(),
        )

        db.session.add(new_note) 
        db.session.commit()

    @classmethod
    def can_see_notes(cls, id_user: int, request_id: int)->bool:
        """
        Checks if the user can see the notes of the requirement
        or add one
        """
        return True if Requirement.query.filter_by(id=request_id, user_id=id_user).first() else False


    
