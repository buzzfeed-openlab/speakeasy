from flask_sqlalchemy import SQLAlchemy
from story_collector import create_app


app = create_app()
db = SQLAlchemy(app)