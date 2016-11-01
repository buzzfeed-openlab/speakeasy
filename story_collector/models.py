import datetime

from story_collector.database import db


class Story(db.Model):
    # TODO: add extra demographic info
    id = db.Column(db.Integer, primary_key=True)
    call_sid = db.Column(db.String(255), unique=True)
    from_number = db.Column(db.String(255))
    recording_url = db.Column(db.String(255), unique=True)
    is_approved = db.Column(db.Boolean, default=False)
    dt = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, call_sid, from_number, recording_url):
        self.call_sid = call_sid
        self.from_number = from_number
        self.recording_url = recording_url


    def __repr__(self):
        return '<Story %r>' % self.recording_url