from story_collector.database import db


class Story(db.Model):
	# TODO: add phone num, moderator approval flag, extra demographic info
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), unique=True)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<Story %r>' % self.url