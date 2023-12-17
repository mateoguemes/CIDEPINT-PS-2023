from src.models.state import State
from src.models.database import db

def run():
    create_states()

def create_states():
    states_names = [
        "Cancelado", "Aceptado", "Finalizado", "Pendiente" 
    ]
    # Se crean en la BD
    states = []
    for name in states_names:
        state = State(name)
        states.append(state)
    db.session.add_all(states)
    db.session.commit()



