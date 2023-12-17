from src.models.seeds import roles_and_permissions_seed
from src.models.seeds import institutions_and_services_seed
from src.models.seeds import users_seed
from src.models.seeds import config_seed
from src.models.seeds import states_seed

def run():
    roles = roles_and_permissions_seed.run()
    institutions = institutions_and_services_seed.run()
    users_seed.run(institutions, roles)
    config_seed.run()
    states_seed.run()
    print("terminé")