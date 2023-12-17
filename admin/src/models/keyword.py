from datetime import datetime
from src.models.database import db
from src.models.institution_keyword import Institution_Keyword
from src.models.service_keyword import Service_Keyword

class Keyword(db.Model):
    __tablename__="keywords"
    id = db.Column(db.Integer, primary_key=True, unique= True)
    name = db.Column(db.String(50), nullable=False, unique= True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    inserted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self,name):
        self.name=name

    @classmethod
    def max_length_name(cls)->int:
        """
        Returns the maximum length of the name field.
        """
        return 50
    
    def if_alone_delete(self)->None:
        """
        Deletes the keyword if it is not related to any institution or service.
        """
        relations_with_institutions = Institution_Keyword.query.filter_by(keyword_id=self.id).first()
        relations_with_services = Service_Keyword.query.filter_by(keyword_id=self.id).first()
        if not (relations_with_institutions or relations_with_services):
            db.session.delete(self)
            db.session.commit()
        