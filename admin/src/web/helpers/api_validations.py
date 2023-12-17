from src.models.requirement import Requirement
from src.models.database import db

def valid_data(data: dict)->bool:
    """
    Raises an exception if the data is invalid
    """
    if (not data['description'] or not data['service_id'] or not data['creation_date']):
        raise ValueError
    
    if (len(data['description']) > 255):
        raise ValueError
    

def can_see_data(id_user: int, request_id: int)->bool:
    """
    Checks if the user can see the requirement or notes
    """
    return True if Requirement.query.filter_by(id=request_id, user_id=id_user).first() else False
    

    
