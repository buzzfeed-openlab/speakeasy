from flask import redirect, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from story_collector import create_app
from story_collector.app_config import ADMIN_USER, ADMIN_PASS
from story_collector.models import Story
from story_collector.database import db
import twilio.twiml


app = create_app()

@app.route("/")
def index():
    # TODO: grab some recordings to show
    return render_template('index.html')

@app.route('/browse')
def browse():
    approved = Story.query.filter_by(is_approved=True).all()
    return render_template('browse.html', approved=approved)


@app.route("/greet", methods=['GET', 'POST'])
def greet():
    """Respond to incoming requests."""
    print("greet")
    resp = twilio.twiml.Response()
    resp.say("Hi stranger. Tell me your election 2016 secrets. You have 30 seconds after the tone.")
    resp.record(maxLength="30", action="/handle-recording")

    return str(resp)

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""

    recording_url = request.values.get('RecordingUrl', None)
    call_sid = request.values.get('CallSid', None)
    from_number = request.values.get('From', None)

    resp = twilio.twiml.Response()
    resp.say("Thanks! Here is your recording:")
    resp.play(recording_url)

    print("recording url: %s" %recording_url)

    new_story = Story(call_sid, from_number, recording_url)
    db.session.add(new_story)
    db.session.commit()

    # TODO: handle re-recording
    # TODO: collect demographic info

    return str(resp)


# @app.route("/handle-key", methods=['GET', 'POST'])
# def handle_key():
#     """Handle key press from a user."""

#     # Get the digit pressed by the user
#     digit_pressed = request.values.get('Digits', None)
#     if digit_pressed == "1":
#         resp = twilio.twiml.Response()
#         resp.say("you pressed 1")
#         return str(resp)
#     else:
#     	resp.say("you pressed something else")
#     	return str(resp)


#     # # If the caller pressed anything but 1, redirect them to the homepage.
#     # else:
#     #     return redirect("/")


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
    review_queue = Story.query.filter_by(is_approved=False).all()
    approved = Story.query.filter_by(is_approved=True).all()
    return render_template('review.html', review_queue = review_queue, approved=approved)

@app.route('/approve/<story_id>')
@requires_auth
def approve(story_id):
    story = Story.query.get(story_id)
    story.is_approved = True
    return redirect('/review')

@app.route('/disapprove/<story_id>')
@requires_auth
def disapprove(story_id):
    story = Story.query.get(story_id)
    story.is_approved = False
    return redirect('/review')



if __name__ == "__main__":
    app.run(debug=True)