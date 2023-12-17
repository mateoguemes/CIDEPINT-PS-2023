from src.web import create_app
#from src.models import database
from flask_cors import CORS

#from pathlib import Path

#static_folder = Path(__file__).parent.absolute().joinpath("public")
app = create_app()
if __name__ == "__main__":
    app.run()