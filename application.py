from flask import redirect, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func
from functools import wraps
from story_collector import create_app, db
from story_collector.app_config import ADMIN_USER, ADMIN_PASS, USE_FAKE_DATA, APP_URL, NOTIFY_FROM_NUM, NOTIFY_TO_NUM, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from story_collector.models import Story
from story_collector.fake_data import FAKE_STORIES
import twilio.twiml
from twilio.rest import TwilioRestClient


application = create_app()

if NOTIFY_FROM_NUM and NOTIFY_TO_NUM and TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    try:
        twilio_client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    except twilio.exceptions.TwilioException:
        twilio_client = None


@application.route("/", methods=['GET', 'POST'])
def index():
    """Respond to incoming requests."""
    print("greet")
    resp = twilio.twiml.Response()
    resp.play(APP_URL+'/static/assets/greet.mp3')
    resp.record(maxLength="30", action="/handle-recording")

    if twilio_client:
        notify('someone called!')

    return str(resp)


@application.route('/browse')
def browse():

    if USE_FAKE_DATA:
        approved = FAKE_STORIES
    else:
        approved = Story.query.filter_by(is_approved=True).all()

    return render_template('browse.html', approved=approved)


@application.route("/handle-recording", methods=['GET', 'POST'])
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

    # # collecting zip
    # resp.play('http://lamivo.com/wwtd/collect_zip.mp3')
    # resp.gather(numDigits=5, action="/collect-zip", method="POST")
    # resp.pause(length=20)


    # get a random story that has been approved and play it
    print("grabbing a random story")
    random_story = Story.query.filter_by(is_approved=True).order_by(func.rand()).first()

    if random_story:
        resp.play(APP_URL+'/static/assets/thanks.mp3')
        resp.pause(length=1)
        resp.play(random_story.recording_url)
        resp.pause(length=3)
        resp.play(APP_URL+'/static/assets/bye.mp3')

    notify("recorded: %s \nreceived: %s" %(new_story.recording_url, random_story.recording_url))

    return str(resp)


@application.route("/collect-zip", methods=['GET', 'POST'])
def collect_zip():

    pressed = request.values.get('Digits', None)

    story = Story.query.filter_by(call_sid=request.values.get('CallSid', None)).first()
    story.caller_zip = pressed
    db.session.commit()

    resp = twilio.twiml.Response()
    # resp.play('http://lamivo.com/wwtd/outro.mp3')
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


@application.route('/review')
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

@application.route('/approve/<story_id>')
@requires_auth
def approve(story_id):
    story = Story.query.get(story_id)
    story.is_approved = True
    db.session.commit()
    return redirect('/review')

@application.route('/disapprove/<story_id>')
@requires_auth
def disapprove(story_id):
    story = Story.query.get(story_id)
    story.is_approved = False
    db.session.commit()
    return redirect('/review')


@application.route('/initialize')
@requires_auth
def initialize():
    print("\nINITIALIZING DB")

    # TODO: only do this if tables don't exist?
    print("  * making sure all tables have been created")
    db.create_all()

    # TODO: add stuff to create some admin users for moderation

    # adding some initial responses
    print("  * seeding the db with a response")
    if not Story.query.filter_by(call_sid='seed1').first():
        # this is lam's story about being an immigrant
        rec = Story('seed1', '', 'https://api.twilio.com/2010-04-01/Accounts/AC8820553f8206a5c5f7608355621ccd90/Recordings/RE6ebf1e9bbfc378667985b9bdf032ebac')
        rec.is_approved = True
        db.session.add(rec)
        db.session.commit()
        print("      ...OK!")
    else:
        print("      ...already done previously")

    return redirect('/')

def notify(msg):
    twilio_client.messages.create(to=NOTIFY_TO_NUM, from_=NOTIFY_FROM_NUM, body=msg)



if __name__ == "__main__":
    application.run(debug=True, host='0.0.0.0')