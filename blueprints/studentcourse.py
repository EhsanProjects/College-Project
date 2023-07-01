from flask import Blueprint
import models.studentcourse
app = Blueprint("studentcourse", __name__)

@app.route('/studentcourse')
def studentcourse():  # put application's code here
    return 'This is studentcourse page!'


