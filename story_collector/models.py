import datetime

from . import db


class Story(db.Model):
    # TODO: add extra demographic info
    id = db.Column(db.Integer, primary_key=True)
    call_sid = db.Column(db.String(255), unique=True)
    from_number = db.Column(db.String(255))
    recording_url = db.Column(db.String(255), unique=True)
    is_approved = db.Column(db.Boolean)
    dt = db.Column(db.DateTime, default=datetime.datetime.now)
    caller_zip = db.Column(db.String(255))
    to_number = db.Column(db.String(255))
    test_version = db.Column(db.String(255))

    def __init__(self, call_sid, from_number, to_number, recording_url, test_version=None):
        self.call_sid = call_sid
        self.from_number = from_number
        self.recording_url = recording_url
        self.to_number = to_number

    def __repr__(self):
        return '<Story %r>' % self.recording_url
