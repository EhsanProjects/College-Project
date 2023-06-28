from flask import Blueprint
import models.student
app = Blueprint("student", __name__)

@app.route('/student')
def student():  # put application's code here
    return 'This is student page!'


