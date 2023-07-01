from flask import Flask
from flask_wtf.csrf import CSRFProtect
from blueprints.general import app as general
from blueprints.student import app as student
from blueprints.instructor import app as instructor

from blueprints.admin import app as admin
import config
import extentions

app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(student)
app.register_blueprint(instructor)

app.register_blueprint(admin)


app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
extentions.db.init_app(app)

csrf = CSRFProtect(app)

with app.app_context():
    extentions.db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
