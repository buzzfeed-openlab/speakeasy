from flask import redirect, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from story_collector import create_app
from story_collector.app_config import ADMIN_USER, ADMIN_PASS, USE_FAKE_DATA
from story_collector.models import Story
from story_collector.database import db
from story_collector.fake_data import FAKE_STORIES
import twilio.twiml


app = create_app()

@app.route("/")
def index():
    # TODO: grab some recordings to show
    return render_template('index.html')

@app.route('/browse')
def browse():

    if USE_FAKE_DATA:
        approved = FAKE_STORIES
    else:
        approved = Story.query.filter_by(is_approved=True).all()

    return render_template('browse.html', approved=approved)


@app.route("/greet", methods=['GET', 'POST'])
def greet():
    """Respond to incoming requests."""
    print("greet")
    resp = twilio.twiml.Response()
    resp.play('http://lamivo.com/wwtd/greet.mp3')
    resp.record(maxLength="30", action="/handle-recording")


    
    return str(resp)

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""

    recording_url = request.values.get('RecordingUrl', None)
    call_sid = request.values.get('CallSid', None)
    from_number = request.values.get('From', None)

    resp = twilio.twiml.Response()

    # resp.say("Thanks! Here is your recording:")
    # resp.play(recording_url)
    # # TODO: handle re-recording

    print("recording url: %s" %recording_url)

    new_story = Story(call_sid, from_number, recording_url)
    db.session.add(new_story)
    db.session.commit()

    # collecting zip
    resp.play('http://lamivo.com/wwtd/collect_zip.mp3')
    resp.gather(numDigits=5, action="/collect-zip", method="POST")

    resp.pause(length=20)
    return str(resp)


@app.route("/collect-zip", methods=['GET', 'POST'])
def collect_zip():

    pressed = request.values.get('Digits', None)

    story = Story.query.filter_by(call_sid=request.values.get('CallSid', None)).first()
    story.caller_zip = pressed
    db.session.commit()

    resp = twilio.twiml.Response()
    resp.play('http://lamivo.com/wwtd/outro.mp3')
    return str(resp)


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    return username == ADMIN_USER and password == ADMIN_PASS

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your credentials for that url', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@app.route('/review')
@requires_auth
def review():
    if USE_FAKE_DATA:
        review_queue = FAKE_STORIES
        approved = FAKE_STORIES
        disapproved = FAKE_STORIES
    else:
        review_queue = Story.query.filter_by(is_approved=None).all()
        approved = Story.query.filter_by(is_approved=True).all()
        disapproved = Story.query.filter_by(is_approved=False).all()

    return render_template('review.html', review_queue = review_queue, approved=approved, disapproved=disapproved)

@app.route('/approve/<story_id>')
@requires_auth
def approve(story_id):
    story = Story.query.get(story_id)
    story.is_approved = True
    db.session.commit()
    return redirect('/review')

@app.route('/disapprove/<story_id>')
@requires_auth
def disapprove(story_id):
    story = Story.query.get(story_id)
    story.is_approved = False
    db.session.commit()
    return redirect('/review')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')