from datetime import datetime
from src.models.database import db

class Permission(db.Model):
    __tablename__="permissions"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    name = db.Column(db.String(50), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,name):
        self.name=name
        db.session.add(self)
        db.session.commit()

    def get_names(ids:int)->list:
        """
        Returns a list of names of the permissions with the given ids.
        """
        names = []
        for id in ids:
            names.append(Permission.query.filter_by(id=id).first().name)
        return names
