from story_collector.database import db
from story_collector.models import Story


def init_db():

    print("\nINITIALIZING DB")

    # TODO: only do this if tables don't exist?
    db.create_all()

	# TODO: add stuff to create some admin users for moderation


if __name__ == "__main__":
    init_db()
    print("done!")