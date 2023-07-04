from flask import Blueprint, render_template, request, session, redirect, abort, url_for
import config
from datetime import datetime
from blueprints.student import student
from models.department import Department
from models.student import Student
from models.course import Course
from models.instructor import Instructor
# from models.studentcourse import Studentcourse
from models.studentinfo import StudentInfo

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


@app.route('/admin/dashboard/students', methods=["GET", "POST"])
def students():
    if request.method == "GET":
        students = Student.query.all()
        return render_template("admin/student.html", students=students)
    else:
        LastName = request.form.get('LastName', None)
        FirstName = request.form.get('FirstName', None)
        Major = request.form.get('Major', None)
        EnrollmentDate = request.form.get('EnrollmentDate')
        #EnrollmentDate ='01-01-2021'
        GraduationDate = request.form.get('GraduationDate')

        stu = Student(LastName=LastName.title(), FirstName=FirstName.title(), Major=Major.title(),
                      EnrollmentDate=EnrollmentDate, GraduationDate=GraduationDate)

        db.session.add(stu)
        db.session.commit()
        return "Done"


@app.route('/admin/dashboard/edit-student/<StudentID>', methods=["GET", "POST"])
def edit_student(StudentID):
    student = Student.query.filter(Student.StudentID == StudentID).first_or_404()
    if request.method == "GET":
        return render_template("admin/edit-student.html", student=student)
    else:
        LastName = request.form.get('LastName', None)
        FirstName = request.form.get('FirstName', None)
        Major = request.form.get('Major', None)
        EnrollmentDate = request.form.get('EnrollmentDate')
        GraduationDate = request.form.get('GraduationDate')

        student.LastName = LastName
        student.FirstName = FirstName
        student.Major = Major
        student.EnrollmentDate = EnrollmentDate
        student.GraduationDate = GraduationDate
        # db.session.add(dept)
        db.session.commit()
        #return "Information Edited."
        return redirect(url_for("admin.edit_student", StudentID=StudentID))


@app.route('/admin/dashboard/courses', methods=["GET", "POST"])
def courses():
    if request.method == "GET":
        courses = Course.query.all()
        return render_template("admin/course.html", courses=courses)
    else:
        CourseNumber = request.form.get('CourseNumber', None)

        cors = Course(CourseNumber=CourseNumber.title())

        db.session.add(cors)
        db.session.commit()
        return "Done"
