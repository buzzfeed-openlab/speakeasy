from story_collector.database import db
from story_collector.models import Story


def init_db():

    print("\nINITIALIZING DB")

    # TODO: only do this if tables don't exist?
    print("  * making sure all tables have been created")
    db.create_all()

	# TODO: add stuff to create some admin users for moderation

    # adding some initial responses
    seed_db()


def seed_db():

    # this is lam's story about being an immigrant
    print("  * seeding the db with a response")
    if not Story.query.filter_by(call_sid='seed1').first():
        rec = Story('seed1', '', 'https://api.twilio.com/2010-04-01/Accounts/AC8820553f8206a5c5f7608355621ccd90/Recordings/RE6ebf1e9bbfc378667985b9bdf032ebac')
        rec.is_approved = True
        db.session.add(rec)
        db.session.commit()
        print("      ...OK!")
    else:
        print("      ...already done previously")



if __name__ == "__main__":
    init_db()
    print("done initializing db!")