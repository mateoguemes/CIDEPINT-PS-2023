from datetime import datetime
from enum import Enum as PythonEnum
from src.models.keyword import Keyword
from src.models.service_keyword import Service_Keyword
from sqlalchemy import Enum
from src.models.database import db
from src.models.institution_service import Institution_Service

class ServiceType(PythonEnum):
   ANALYSIS = "Análisis"
   CONSULTING = "Consultoría"
   DEVELOPMENT = "Desarrollo"

   @classmethod
   def string_to_service_type(cls, string:str)->object:
       """
       Returns the ServiceType object that corresponds to the given string.
       """
       for member in ServiceType:
           if string == member.value:
               return member
       return None #si la cadena no es válida
  
   @classmethod
   def get_all_values(cls) -> list:
       """
       Returns a list with all types of services.
       """
       return [member.value for member in cls]

class Service(db.Model):
   __tablename__ = "services"
   id = db.Column(db.Integer, primary_key=True, unique=True)
   name = db.Column(db.String(100), nullable=False)
   description = db.Column(db.String(255), nullable=False)
   type = db.Column(db.Enum(ServiceType), nullable=False)
   enable = db.Column(db.Boolean, nullable=False, default=True)
   updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
   inserted_at = db.Column(db.DateTime, default=datetime.utcnow)
   requirements = db.relationship('Requirement', back_populates='service')
   institutions = db.relationship('Institution_Service', back_populates='service')

   def __init__(self, name, description, type, enable):
       self.name = name
       self.description = description
       self.type = type
       self.enable = enable
  
   def get_keywords(self) -> list:
       """
       Returns a list with the keywords of the service.
       """
       keyword_ids = [relation.keyword_id
                       for relation in
                       Service_Keyword.query.filter_by(service_id=self.id).all()]
       return Keyword.query.filter(Keyword.id.in_(keyword_ids)).all()
  
   def update(self, name: str, description: str, type: str, enable: bool)-> None:
       """
       Updates the attributes of the service.
       """
       self.name = name
       self.description = description
       self.type = type
       self.enable = enable

   def __eq__(self, other):
       return self.name == other.name

   def __le__(self, other):
       return self.name <= other.name

   def __lt__(self, other):
       return self.name < other.name
  
   @classmethod
   def is_this_name_unique_for(cls, name: str, institution_id: int)-> bool:
       """
       This method checks if the given name is
       unique among the services of the specified institution
       """
       institution_service_ids = [service.service_id
                                  for service
                                  in Institution_Service.query
                                  .filter_by(institution_id=institution_id).all()]
       existing_service = Service.query.filter(
           Service.id.in_(institution_service_ids),
           Service.name == name
       ).first()
       return existing_service is None
  
   @classmethod
   def can_update_name_to(cls, name: str, institution_id: int, service_id:int)-> bool:
       """
       This method checks if the given name
       can be used for the update of a service
       """
       institution_service_ids = [service.service_id for service in Institution_Service.query.filter_by(institution_id=institution_id).all()]
      
       existing_service = Service.query.filter(
           Service.id.in_(institution_service_ids),
           Service.name == name,
       ).first()
      
       return (existing_service is None) or existing_service.id == service_id

   def api_services_search(services: list)-> list:
       """
       Returns a list of dictionaries with the following structure:
       [
           {
               "name": "service_name",
               "description": "service_description",
               "keywords": ["keyword1", "keyword2", ...],
               "laboratory": "laboratory_name",
               "enabled": "true/false",
           },
       ]
       Method used to adapt the information of the services to the format required by the frontend.
       """
       result = []
       for service in services:
           keywords = service.get_keywords()
           institutions = service.institutions
           laboratory = institutions[0].institution.name if institutions else None

           result.append({
               "name": service.name,
               "description": service.description,
               "keywords": [keyword.name for keyword in keywords],
               "laboratory": laboratory,
               "enabled": service.enable,
           })
       return result
  
   def api_get_service(self)-> list:
       """
       Returns a service in a list of dictionaries with the following structure:
       [
           {
               "id": "service_id"
               "name": "service_name",
               "description": "service_description",
               "keywords": ["keyword1", "keyword2", ...],
               "laboratory": "laboratory_name",
               "enabled": "true/false",
           },
       ]
       """
       result = []
      
       keywords = self.get_keywords()
       institutions = self.institutions
       laboratory = institutions[0].institution.name if institutions else None

       result.append({
           "id": self.id,
           "name": self.name,
           "description": self.description,
           "keywords": [keyword.name for keyword in keywords],
           "laboratory": laboratory,
           "enabled": self.enable,
       })
       return result
  
   def api_get_services_for_form(services: list)->list:
       """
       Returns a list of dictionaries with the following structure:
       [
           {
               "name": "service_name",
               "description": "service_description",
               "id": "service_id",
           },
       ]
       """
       result = []
       for service in services:
           result.append({
               "name": service.name,
               "description": service.description,
               "id": service.id,
           })
       return result
