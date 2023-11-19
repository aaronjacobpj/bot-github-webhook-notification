from .bots import *

from flask import current_app as app
from flask import request, jsonify




@app.route("/google-space/git-push", methods=["POST"])
def google_space_git_push():
    """
    End point for send notification to google space.
    """

    GOOGLE_BOT.send_git_push_notification(request.json)
    return jsonify({"message": "Request Successful"})


