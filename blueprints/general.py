from flask import Blueprint, render_template

app = Blueprint("general", __name__)

@app.route('/')
def main():  # put application's code here
    return  render_template('main.html')


@app.route('/help')
def help():  # put application's code here
    return  render_template('help.html')