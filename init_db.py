from flask.ext.sqlalchemy import SQLAlchemy
from story_collector import create_app
from story_collector.models import Story
from story_collector.database import db


def init_db():

    print("\nINITIALIZING DB")

    # TODO: only do this if tables don't exist?
    db.create_all()

	# TODO: add stuff to create some admin users for moderation


if __name__ == "__main__":
    init_db()
    print("done!")