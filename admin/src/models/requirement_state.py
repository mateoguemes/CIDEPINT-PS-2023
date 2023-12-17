from datetime import datetime
from src.models.database import db
from src.models.state import State

class Requirement_State(db.Model):
    __tablename__ = "requirement_state"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    observation = db.Column(db.String(255), nullable=False)
    requirement_id = db.Column(db.Integer, db.ForeignKey("requirements.id"), nullable=False) 
    state_id = db.Column(db.Integer, db.ForeignKey("states.id"), nullable=False, default=4) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  #this is the date of the change of state
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
    state = db.relationship('State', backref='requirement_states', foreign_keys=[state_id])
    
    @classmethod
    def update_requirement_state(cls, requirement_state: object,
                                  new_state_id:str, new_observation:str)->None:
        """
        Updates the state of a requirement.
        """
        requirement_state.state_id = new_state_id
        requirement_state.observation = new_observation
        db.session.commit()
