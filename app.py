from flask import Flask
from blueprints.general import app as general
from blueprints.student import app as student
from blueprints.admin import app as admin
import config
import extentions

app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(student)
app.register_blueprint(admin)


app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
extentions.db.init_app(app)

with app.app_context():
    extentions.db.create_all()

if __name__ == '__main__':
    app.run()
