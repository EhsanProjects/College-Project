from flask import Blueprint
import models.instructor
app = Blueprint("instructor", __name__)

@app.route('/instructor')
def instructor():  # put application's code here
    return 'This is instructor page!'


