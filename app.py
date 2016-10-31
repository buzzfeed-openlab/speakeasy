from flask import request, render_template
from flask_sqlalchemy import SQLAlchemy
import twilio.twiml
from story_collector import create_app
from story_collector.models import Story
from story_collector.database import db


app = create_app()

@app.route("/")
def index():
    # TODO: grab some recordings to show
    return render_template('index.html')


@app.route("/greet", methods=['GET', 'POST'])
def greet():
    """Respond to incoming requests."""
    print("greet")
    resp = twilio.twiml.Response()
    resp.say("Hi stranger. Tell me your election 2016 secrets. You have 5 seconds after the tone.")
    resp.record(maxLength="5", action="/handle-recording")

    return str(resp)

@app.route("/handle-recording", methods=['GET', 'POST'])
def handle_recording():
    """Play back the caller's recording."""

    recording_url = request.values.get("RecordingUrl", None)

    resp = twilio.twiml.Response()
    resp.say("Thanks! Here is your recording:")
    resp.play(recording_url)

    print("recording url: %s" %recording_url)

    new_story = Story(recording_url)
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


if __name__ == "__main__":
    app.run(debug=True)