from flask import Blueprint

app = Blueprint("general", __name__)

@app.route('/')
def main():  # put application's code here
    return 'This is main page!'


@app.route('/help')
def help():  # put application's code here
    return 'Help page!'