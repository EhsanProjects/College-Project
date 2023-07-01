from flask import Blueprint, render_template, request, session, redirect, abort, url_for
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

        dept = Department(DepartmentName=DepartmentName.title())

        db.session.add(dept)
        db.session.commit()
        return "Done"


@app.route('/admin/dashboard/edit-department/<DepartmentID>', methods=["GET", "POST"])
def edit_department(DepartmentID):
    department = Department.query.filter(Department.DepartmentID == DepartmentID).first_or_404()
    if request.method == "GET":
        return render_template("admin/edit-department.html", department=department)
    else:
        DepartmentName = request.form.get('DepartmentName', None)
        department.DepartmentName = DepartmentName.title()

        # db.session.add(dept)
        db.session.commit()
        return redirect(url_for("admin.edit_department", DepartmentID=DepartmentID))


