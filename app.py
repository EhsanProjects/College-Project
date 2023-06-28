from flask import Flask
from blueprints.general import app as general
from blueprints.student import app as student
from blueprints.admin import app as admin

app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(student)
app.register_blueprint(admin)


if __name__ == '__main__':
    app.run()
