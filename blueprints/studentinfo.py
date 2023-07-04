from flask import Blueprint
import models.studentinfo
app = Blueprint("studentinfo", __name__)

@app.route('/studentinfo')
def studentinfo():  # put application's code here
    return 'This is studentinfo page!'


