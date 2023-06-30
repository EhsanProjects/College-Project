from flask import Blueprint, render_template, request, session, redirect, abort
import config
from models.department import Department
from extentions import db

app = Blueprint("admin", __name__)


@app.before_request
def before_request():
    if session.get('admin_login', None) == None and request.endpoint != "admin.login":
        abort(403)


@app.route('/admin/login', methods=["POST", "GET"])
def login():  # put application's code here
    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        print(username, password)
        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session['admin_login'] = username
            return redirect("/admin/dashboard")
        else:
            return redirect("/admin/login")
    else:
        return render_template("admin/login.html")


@app.route('/admin/dashboard', methods=["GET"])
def dashboard():
    return render_template("admin/dashboard.html")


@app.route('/admin/dashboard/departments', methods=["GET", "POST"])
def departments():
    if request.method == "GET":
        departments = Department.query.all()
        return render_template("admin/department.html", departments=departments)
    else:
        DepartmentName = request.form.get('DepartmentName', None)

        dept = Department(DepartmentName=DepartmentName)

        db.session.add(dept)
        db.session.commit()
        return "Done"
