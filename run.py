import os
from dotenv import load_dotenv
from flask_migrate import Migrate

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from project import create_app, db

# Start the server
app = create_app(os.getenv("FLASK_CONFIG") or "default")

migrate = Migrate(app, db)
