from flask import Blueprint

app = Blueprint("student", __name__)

@app.route('/student')
def student():  # put application's code here
    return 'This is student page!'


