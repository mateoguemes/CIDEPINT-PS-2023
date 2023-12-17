from src.models.user import User
from src.models.keyword import Keyword
import re

def valid_email(form: dict)->bool:
    """
    Returns False if the email is already in use by another user, True otherwise
    """
    mail_in_use = User.user_exists(form['email']) != None # Si el mail esta en uso, devuelve True, sino False
    if (mail_in_use):
        mail_is_mine = User.user_exists(form['email']).id == int(form['id']) # Si el mail es mio, devuelve True, sino False
    else:
        mail_is_mine = False
    return True if (not mail_in_use) or (mail_is_mine) else False

def validate_entry_data(form: dict)->bool:
    """Validates the correctness of the data"""
    # Que pasa si cambio el type de algun campo del formulario?
    keys = form.keys()
    for key in keys:
        if form[key] == '':
            return False
    try: # Por si cambia el nombre de los campos del formulario
        if (len(form['name']) or len(form['lastname'])) > 255:
            return False

        if (len(form['email']) or len(form['username']) ) > 255:
            return False
        
        if not (re.match(r'^[a-zA-Z\s]+$', form['name']) or (re.match(r'^[a-zA-Z\s]+$', form['lastname']))):
            return False
        
        if not (re.match(r"[^@]+@[^@]+\.[^@]+", form['email'])):
            return False
    except:
        return False

    return True    
