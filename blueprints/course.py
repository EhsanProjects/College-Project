from flask import Blueprint
import models.course
app = Blueprint("course", __name__)

@app.route('/course')
def course():  # put application's code here
    return 'This is course page!'


