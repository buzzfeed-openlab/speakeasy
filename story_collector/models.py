from story_collector.database import db


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(120), unique=True)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<Story %r>' % self.url