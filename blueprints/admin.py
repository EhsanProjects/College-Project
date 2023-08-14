import sqlite3

from flask import Blueprint, render_template, request, session, redirect, abort, url_for, jsonify, flash
from sqlalchemy import text, and_, engine

from sqlalchemy.engine import cursor
from datetime import datetime, date

from sqlalchemy.exc import SQLAlchemyError

import config

from blueprints.student import student
from models.department import Department
from models.major import Major
from models.student import Student
from models.course import Course
from models.instructor import Instructor
from models.studentcourse import Studentcourse

from models.studentinfo import StudentInfo

from extentions import db

app = Blueprint("admin", __name__)


@app.before_request
def before_request():
    if session.get('admin_login', None) == None and request.endpoint != "admin.login":
        abort(403)


@app.route('/logout')
def logout():
    # Clear the session data
    session.clear()
    # Redirect to the login page
    return redirect(url_for('admin.login'))


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
        # return "Done"
        flash("Department added Successfully.", "Success")
        return redirect(url_for("admin.dashboard"))


@app.route('/admin/dashboard/edit-department/<DepartmentID>', methods=["GET", "POST"])
def edit_department(DepartmentID):
    department = Department.query.filter(Department.DepartmentID == DepartmentID).first_or_404()
    if request.method == "GET":
        return render_template("admin/edit-department.html", department=department)
    else:
        if DepartmentID:
            DepartmentName = request.form.get('DepartmentName', None)
            department.DepartmentName = DepartmentName.title()
            db.session.commit()
            flash("Department Edited Successfully.", "Success")
        else:
            flash("Error: Please call Network Administrator", "error")
        return redirect(url_for("admin.dashboard"))


# ------------------------------------------
@app.route('/admin/dashboard/majors', methods=["GET", "POST"])
def majors():
    if request.method == "GET":

        majors = Major.query.all()
        return render_template("admin/major.html", majors=majors)
    else:
        MajorName = request.form.get('MajorName', None)
        mjr = Major(MajorName=MajorName.title())

        db.session.add(mjr)
        db.session.commit()
        flash("Major added Successfully.", "Success")
        return redirect(url_for("admin.dashboard"))


@app.route('/admin/dashboard/edit-major/<MajorID>', methods=["GET", "POST"])
def edit_major(MajorID):
    major = Major.query.filter(Major.MajorID == MajorID).first_or_404()

    if request.method == "GET":
        return render_template("admin/edit-major.html", major=major)
    else:
        if MajorID:
            MajorName = request.form.get('MajorName', None)
            major.MajorName = MajorName.title()

            # db.session.add(dept)
            db.session.commit()
            # return redirect(url_for("admin.edit_major", MajorID=MajorID))
            # return redirect(url_for("admin.edit_major", MajorID=MajorID))
            flash("Major Edited Successfully.", "Success")

        else:
            flash("Error: Please call Network Administrator", "error")
    return redirect(url_for("admin.dashboard"))


# ------------------------------------------

@app.route('/admin/dashboard/students', methods=["GET", "POST"])
def students():
    if request.method == "POST":

        LastName = request.form.get('LastName', None).title()
        FirstName = request.form.get('FirstName', None).title()
        MajorID = request.form.get('MajorID', None).title()
        EnrollmentDate = request.form.get('EnrollmentDate')

        GraduationDate = request.form.get('GraduationDate', None)

        if GraduationDate:
            if GraduationDate == 'None':
                GraduationDate = ''

            else:

                GraduationDate = datetime.strptime(GraduationDate, '%Y-%m-%d')
        else:
            GraduationDate = None

        file = request.files.get('img', None)
        stu = Student(LastName=LastName.title(), FirstName=FirstName.title(), MajorID=MajorID,
                      EnrollmentDate=EnrollmentDate, GraduationDate=GraduationDate)

        db.session.add(stu)
        db.session.commit()
        file.save(f'static/img/{stu.StudentID}.jpg')

        # Extract the form data
        dob_str = request.form.get("Dob")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()  # Convert the date string to a Python date object
        phone = request.form.get("Phone")
        address = request.form.get("Address")
        city = request.form.get("City").title()
        state = request.form.get("State").title()
        zipcode = request.form.get("Zipcode")
        email = request.form.get("Email").title()
        student_id = stu.StudentID

        # Save the form data to the studentinfo table using SQLAlchemy

        student_info = StudentInfo(
            Dob=dob,
            Phone=phone,
            Address=address.title(),
            City=city.title(),
            State=state.title(),
            Zipcode=zipcode,
            Email=email.title(),
            StudentID=student_id
        )

        db.session.add(student_info)
        db.session.commit()

        # Return a JSON response indicating success
        # return jsonify({"message": "Student information added Successfully."}), 200
        flash("Student added Successfully.", "Success")
        return redirect(url_for("admin.dashboard"))
    else:
        query = text(
            'SELECT majors.MajorID, majors.MajorName FROM majors order by majors.MajorName')
        majors = db.session.execute(query)
        # Convert the query result to a list of tuples
        majors = [(row[0], row[1]) for row in majors]

        query3 = text(
            'SELECT students.StudentID,students.LastName,students.FirstName,students.EnrollmentDate,students.GraduationDate,students.MajorID, majors.MajorName FROM students '
            ' join   majors ON students.MajorID = majors.MajorID order by students.LastName')
        students = db.session.execute(query3)
        # Convert the query result to a list of tuples
        students = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in students]

        return render_template("admin/student.html", students=students, majors=majors)
        # return render_template("admin/student.html")


@app.route('/admin/dashboard/edit-student/<StudentID>', methods=["GET", "POST"])
def edit_student(StudentID):
    thismajor = StudentID
    student = Student.query.filter_by(StudentID=StudentID).first_or_404()
    studentinfo = StudentInfo.query.filter_by(StudentID=StudentID).first_or_404()

    # student = Student.query.filter(Student.StudentID == StudentID).first_or_404()
    # studentinfo = StudentInfo.query.filter(StudentInfo.StudentID == StudentID).first_or_404()
    if request.method == "GET":

        query3 = text(
            'SELECT majors.MajorID, majors.MajorName FROM majors  order by majors.MajorName')
        majors = db.session.execute(query3)
        # Convert the query result to a list of tuples
        majors = [(row[0], row[1],) for row in majors]

        query4 = text(
            'SELECT students.StudentID, students.LastName, students.FirstName, students.EnrollmentDate, students.GraduationDate, students.MajorID, majors.MajorName FROM students '
            'JOIN majors ON students.MajorID = majors.MajorID WHERE students.StudentID=:thismajor')
        studentfind = db.session.execute(query4, {'thismajor': thismajor})
        # Convert the query result to a list of tuples
        studentfind = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in studentfind]

        return render_template("admin/edit-student.html", student=student, majors=majors, studentfind=studentfind,
                               studentinfo=studentinfo)
    else:

        if StudentID:

            LastName = request.form.get('LastName', None)
            FirstName = request.form.get('FirstName', None)
            MajorID = request.form.get('MajorID', None)
            EnrollmentDate = request.form.get('EnrollmentDate', None)

            if EnrollmentDate:
                EnrollmentDate = datetime.strptime(EnrollmentDate, '%Y-%m-%d %H:%M:%S.%f')
            else:
                EnrollmentDate = None

            GraduationDate = request.form.get('GraduationDate', None)

            if GraduationDate:
                if GraduationDate == 'None':
                    GraduationDate = ''

                else:

                    GraduationDate = datetime.strptime(GraduationDate, '%Y-%m-%d')
            else:
                GraduationDate = None

            file = request.files.get('img', None)
            student.LastName = LastName.title()
            student.FirstName = FirstName.title()
            student.MajorID = MajorID
            student.EnrollmentDate = EnrollmentDate

            if file != None:
                file.save(f'static/img/{student.StudentID}.jpg')
            else:
                flash("Error: New photo has not been saved. Call network administrator.", "error")
            dob_str = request.form.get("Dob", None)

            if dob_str:
                if dob_str == 'None':
                    dob_str = ''

                else:

                    dob_str = datetime.strptime(dob_str, '%Y-%m-%d')
            else:
                dob_str = None

            studentinfo.Dob = dob_str
            studentinfo.Phone = request.form.get("Phone", None)
            studentinfo.Address = request.form.get("Address", None)
            studentinfo.City = request.form.get("City", None).title()
            studentinfo.State = request.form.get("State", None).title()
            studentinfo.Zipcode = request.form.get("Zipcode", None)
            studentinfo.Email = request.form.get("Email", None).title()
            studentinfo.StudentID = thismajor

            try:
                print(thismajor)
                db.session.commit()
                db.session.close()
                flash("Student Edited Successfully.", "Success")
            except Exception as e:
                db.session.rollback()
                flash("Error: " + str(e), "error")

            return redirect(url_for("admin.dashboard"))

            # db.session.commit()

            # flash("Student Edited Successfully.", "Success")
        # else:
        #     flash("Error: Please call Network Administrator", "error")
        # return redirect(url_for("admin.dashboard"))


@app.route('/admin/dashboard/courses', methods=["GET", "POST"])
def get_courses_and_instructors():
    if request.method == "GET":
        # courses = Course.query.all()

        query = text(
            'SELECT departments.DepartmentID, departments.DepartmentName FROM departments order by departments.DepartmentName')
        departments = db.session.execute(query)
        # Convert the query result to a list of tuples
        departments = [(row[0], row[1]) for row in departments]

        query2 = text(
            'SELECT instructors.InstructorID, instructors.FirstName, instructors.LastName FROM instructors order by instructors.LastName')
        instructors = db.session.execute(query2)
        # Convert the query result to a list of tuples
        instructors = [(row[0], row[1], row[2]) for row in instructors]

        query3 = text(
            'SELECT courses.CourseID, courses.CourseNumber, courses.CourseDescription, '
            'courses.CourseUnits, departments.DepartmentName,instructors.FirstName,instructors.LastName FROM departments '
            ' join   courses ON departments.DepartmentID = courses.DepartmentID '
            ' JOIN  instructors  ON courses.InstructorID = instructors.InstructorID order by courses.CourseDescription')
        courses = db.session.execute(query3)
        # Convert the query result to a list of tuples
        courses = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in courses]

        # print(query)
        return render_template("admin/course.html", courses=courses, departments=departments, instructors=instructors)
    if request.method == "POST":
        CourseNumber = request.form.get('CourseNumber', None)
        CourseDescription = request.form.get('CourseDescription', None).title()
        CourseUnits = request.form.get('CourseUnits', None)
        DepartmentID = request.form.get('DepartmentID')
        InstructorID = request.form.get('InstructorID')

        cours = Course(CourseNumber=CourseNumber, CourseDescription=CourseDescription.title(), CourseUnits=CourseUnits,
                       DepartmentID=DepartmentID, InstructorID=InstructorID)

        db.session.add(cours)
        db.session.commit()
        flash("Course added Successfully.", "Success")
        return redirect(url_for("admin.dashboard"))


@app.route('/admin/dashboard/edit-course/<CourseID>', methods=["GET", "POST"])
def edit_course(CourseID):
    course = Course.query.filter(Course.CourseID == CourseID).first_or_404()
    if request.method == "GET":

        query = text(
            'SELECT departments.DepartmentID, departments.DepartmentName FROM departments order by departments.DepartmentName')
        departments = db.session.execute(query)
        # Convert the query result to a list of tuples
        departments = [(row[0], row[1]) for row in departments]

        query2 = text(
            'SELECT instructors.InstructorID, instructors.FirstName, instructors.LastName FROM instructors order by instructors.LastName')
        instructors = db.session.execute(query2)
        # Convert the query result to a list of tuples
        instructors = [(row[0], row[1], row[2]) for row in instructors]

        query3 = text(
            'SELECT courses.CourseID, courses.CourseNumber, courses.CourseDescription, '
            'courses.CourseUnits, departments.DepartmentName,instructors.FirstName,instructors.LastName FROM departments '
            ' join   courses ON departments.DepartmentID = courses.DepartmentID '
            ' JOIN  instructors  ON courses.InstructorID = instructors.InstructorID order by courses.CourseDescription')
        courses = db.session.execute(query3)
        # Convert the query result to a list of tuples
        courses = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in courses]

        # print(query)
        return render_template("admin/edit-course.html", course=course, courses=courses, departments=departments,
                               instructors=instructors)

        # return render_template("admin/edit-course.html", course=course)
    else:
        if CourseID:
            CourseNumber = request.form.get('CourseNumber', None)
            CourseDescription = request.form.get('CourseDescription', None).title()
            CourseUnits = request.form.get('CourseUnits', None)
            DepartmentID = request.form.get('DepartmentID')
            InstructorID = request.form.get('InstructorID')

            course.CourseNumber = CourseNumber
            course.CourseDescription = CourseDescription
            course.CourseUnits = CourseUnits
            course.DepartmentID = DepartmentID
            course.InstructorID = InstructorID
            db.session.commit()
            flash("Course Edited Successfully.", "Success")
        else:
            flash("Error: Please call Network Administrator", "error")
        return redirect(url_for("admin.dashboard"))


@app.route('/admin/dashboard/instructors', methods=["GET", "POST"])
def instructor():
    if request.method == "GET":
        instructors = Instructor.query.all()
        return render_template("admin/instructor.html", instructors=instructors)

    else:
        instructor_count = Instructor.query.count()
        print(instructor_count)
        # Check if the count is more than 0 in order to avoid creating duplicate records.
        if instructor_count > 0:
            flash(
                "Error: It is canceled, in order to avoid creating duplicate records. Please call Network Administrator",
                "error")
            return redirect(url_for("admin.dashboard"))
        else:
            # Created a list of instructors. Because Instrucror table is not one of my requirements I used this list directly.
            # So, many instructors have been added and can be used in Relationship and Reports and Tests.
            new_student = Instructor(LastName='Brown', FirstName='Billy', Status='F', DepartmentChairman=1,
                                     HireDate='2023-07-04 00:30:42.870105', AnnualSalary=77500.0000, DepartmentID=1)
            db.session.add(new_student)

            new_student = Instructor(LastName='Thomas', FirstName='William', Status='P', DepartmentChairman=0,
                                     HireDate='2016-01-04 00:30:42.870105', AnnualSalary=38500.0000, DepartmentID=3)
            db.session.add(new_student)

            new_student = Instructor(LastName='Amundsen', FirstName='Rachel', Status='F', DepartmentChairman=0,
                                     HireDate='2017-01-14 00:30:42.870105', AnnualSalary=79500.0000, DepartmentID=2)
            db.session.add(new_student)

            new_student = Instructor(LastName='Green', FirstName='Gene', Status='F', DepartmentChairman=0,
                                     HireDate='2019-05-04 00:30:42.870105', AnnualSalary=75000.0000, DepartmentID=1)
            db.session.add(new_student)
            new_student = Instructor(LastName='McGregor', FirstName='Bob', Status='F', DepartmentChairman=0,
                                     HireDate='2018-07-04 00:30:42.870105', AnnualSalary=74000.0000, DepartmentID=2)
            db.session.add(new_student)
            new_student = Instructor(LastName='Paxton', FirstName='Arnold', Status='P', DepartmentChairman=0,
                                     HireDate='2023-01-04 00:30:42.870105', AnnualSalary=36000.0000, DepartmentID=3)
            db.session.add(new_student)
            new_student = Instructor(LastName='Smith', FirstName='John', Status='F', DepartmentChairman=1,
                                     HireDate='2022-01-04 00:30:42.870105', AnnualSalary=73000.0000, DepartmentID=2)
            db.session.add(new_student)
            new_student = Instructor(LastName='Connors', FirstName='Daniel', Status='F', DepartmentChairman=0,
                                     HireDate='2021-01-04 00:30:42.870105', AnnualSalary=71500.0000, DepartmentID=4)
            db.session.add(new_student)
            new_student = Instructor(LastName='Jones', FirstName='Sally', Status='F', DepartmentChairman=1,
                                     HireDate='2020-07-04 00:30:42.870105', AnnualSalary=74000.0000, DepartmentID=3)
            db.session.add(new_student)
            new_student = Instructor(LastName='Vilma', FirstName='Jonathan', Status='P', DepartmentChairman=0,
                                     HireDate='2023-07-04 00:30:42.870105', AnnualSalary=35000.0000, DepartmentID=1)
            db.session.add(new_student)
            new_student = Instructor(LastName='Thomas', FirstName='Derrick', Status='P', DepartmentChairman=1,
                                     HireDate='2020-07-04 00:30:42.870105', AnnualSalary=35500.0000, DepartmentID=4)
            db.session.add(new_student)
            new_student = Instructor(LastName='Black', FirstName='Bill', Status='P', DepartmentChairman=0,
                                     HireDate='2022-07-04 00:30:42.870105', AnnualSalary=34000.0000, DepartmentID=4)
            db.session.add(new_student)
            new_student = Instructor(LastName='Warren', FirstName='Angela', Status='P', DepartmentChairman=1,
                                     HireDate='2019-02-04 00:30:42.870105', AnnualSalary=33000.0000, DepartmentID=5)
            db.session.add(new_student)
            new_student = Instructor(LastName='Drew', FirstName='Daniel', Status='F', DepartmentChairman=0,
                                     HireDate='2016-01-04 00:30:42.870105', AnnualSalary=72000.0000, DepartmentID=5)
            db.session.add(new_student)
            new_student = Instructor(LastName='Gallegos', FirstName='Tomas', Status='F', DepartmentChairman=0,
                                     HireDate='2021-01-10 00:30:42.870105', AnnualSalary=64000.0000, DepartmentID=5)
            db.session.add(new_student)

            db.session.commit()
            # Created a list of instructors. Because Instrucror table is not one of my requirements I used this list directly.
            # So, many instructors have been added and can be used in Relationship and Reports and Tests.
            flash(
                "Warning: Created a list of instructors. Because Instrucror table is not one of my requirements I used this list directly.",
                "error")
            flash("Many instructors have been added and can be used in Relationship and Reports and Tests.", "error")
            flash("15 hypothetical Instructures were added, Successfully.", "Success")
            return redirect(url_for("admin.dashboard"))


# -------------------------------------------------------------

@app.route('/admin/dashboard/delete_instructor', methods=['POST'])
def delete_instructor():
    if request.method == 'POST':
        instructor_id = request.form['InstructorID']
        try:
            instructors = Instructor.query.get(instructor_id)
            if instructors:
                db.session.delete(instructors)
                db.session.commit()
                flash('The desired instructor deleted Successfully.', 'Success')
                return redirect(url_for("admin.dashboard"))
        except SQLAlchemyError as e:
            # Handle error, maybe show an error message to the user
            db.session.rollback()
            flash("Error: Please call Network Administrator", "error")
            return redirect(url_for("admin.dashboard"))


# ---------------------------------------------------------------

@app.route('/admin/dashboard/studentcourses', methods=["GET", "POST"])
def studentcourses():
    sid = request.args.get('sid')
    cid = request.args.get('cid')
    # course = Course.query.filter(Course.CourseID == cid).first_or_404()
    # department = Department.query.filter(Department.DepartmentID == course.DepartmentID).first_or_404()

    if request.method == "GET":
        if sid is None and cid is None:
            courses = Course.query.all()
            studentcourses = Student.query.all()

            query = text(
                'SELECT courses.CourseID, courses.CourseNumber, courses.CourseDescription, '
                'courses.CourseUnits, departments.DepartmentName,instructors.FirstName,instructors.LastName FROM departments '
                ' JOIN  courses ON departments.DepartmentID = courses.DepartmentID '
                ' JOIN  instructors  ON courses.InstructorID = instructors.InstructorID order by courses.CourseDescription')

            departments = db.session.execute(query)
            # Convert the query result to a list of tuples
            departments = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in departments]

            # departments = session.query(Department.DepartmentName, Course.CourseID).outerjoin(courses).all()
            return render_template("admin/studentcourse.html", studentcourses=studentcourses, courses=courses,
                                   departments=departments)
        if sid is not None and cid is not None:
            stucourse = Studentcourse(StudentID=sid, CourseID=cid)
            db.session.add(stucourse)
            db.session.commit()

            flash("The desired course added to the student Successfully.", "Success")
            return redirect(url_for("admin.dashboard"))

        if sid is not None or cid is not None:
            flash("Error: Please call IT Administrator.", "error")
            return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        StudentID = request.form.get('sid')
        CourseID = request.form.get('cid')
        if CourseID:
            stucourse = Studentcourse(StudentID=StudentID, CourseID=CourseID)
            db.session.add(stucourse)
            db.session.commit()
            flash('The desired course added to the student Successfully.', 'Success')
            return redirect(url_for("admin.dashboard"))
        else:
            flash('Error: Please select a valid course.', 'error')
            return redirect(url_for("admin.dashboard"))


@app.route('/admin/dashboard/edit-studentcourse/<StudentID>', methods=["GET", "POST"])
def edit_studentcourse(StudentID):
    studentcourse = Studentcourse.query.filter(Student.StudentID == StudentID).first_or_404()
    if request.method == "GET":
        return render_template("admin/edit-studentcourse.html", student=student)
    else:
        LastName = request.form.get('LastName', None)
        FirstName = request.form.get('FirstName', None)
        Major = request.form.get('Major', None)
        EnrollmentDate = request.form.get('EnrollmentDate', '2023-07-06 00:32:27.856366')
        GraduationDate = request.form.get('GraduationDate', None)
        file = request.files.get('img', None)
        studentcourse.LastName = LastName
        studentcourse.FirstName = FirstName
        studentcourse.Major = Major
        studentcourse.EnrollmentDate = EnrollmentDate
        studentcourse.GraduationDate = GraduationDate
        # db.session.add(dept)
        db.session.commit()
        if file != None:
            file.save(f'static/img/{student.StudentID}.jpg')
        # return "Information Edited."
        return redirect(url_for("admin.edit_studentcourse", StudentID=StudentID))


@app.route('/admin/dashboard/instructors/<department_id>')
def get_instructors(department_id):
    # Execute the SQL query based on the department_id
    query = text(
        "SELECT instructors.InstructorID, instructors.FirstName, instructors.LastName FROM instructors WHERE DepartmentID = :department_id")
    instructors = db.session.execute(query, {'department_id': department_id})

    # Convert the result to a list of dictionaries
    results = [dict(row._asdict()) for row in instructors]

    # Prepare the response data
    response = {
        'results': results
    }
    print(query)
    print(response)
    return jsonify(response)


# ------------------------------------------------------------------------
@app.route('/admin/dashboard/studentinfo', methods=["POST"])
def save_student_info():
    if request.method == "POST":
        current_endpoint = request.endpoint
        return f'Current endpoint: {current_endpoint}'

        # Extract the form data
        dob_str = request.form.get("Dob")
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()  # Convert the date string to a Python date object
        phone = request.form.get("Phone")
        address = request.form.get("Address")
        city = request.form.get("City").title()
        state = request.form.get("State")
        zipcode = request.form.get("Zipcode")
        email = request.form.get("Email").title()
        student_id = request.form.get("StudentID")

        # Save the form data to the studentinfo table using SQLAlchemy

        student_info = StudentInfo(
            Dob=dob,
            Phone=phone,
            Address=address,
            City=city,
            State=state,
            Zipcode=zipcode,
            Email=email,
            StudentID=student_id
        )

        db.session.add(student_info)
        db.session.commit()

        # Return a JSON response indicating success
        return jsonify({"message": "Student information added Successfully."}), 200

    # Return an error response if the request method is not POST
    return jsonify({"error": "Invalid request method."}), 400


# ----------------------------------------------------------------
@app.route('/admin/dashboard/delete-major/<int:MajorID>', methods=["POST"])
def delete_major(MajorID):
    try:
        # Retrieve the major with the given MajorID from the database
        major = Major.query.get(MajorID)

        if major:
            # If the major exists, delete it from the database
            db.session.delete(major)
            db.session.commit()
            flash("Major deleted Successfully.", "Success")
        else:
            flash("Error: Major not found.", "error")

    except Exception as e:
        db.session.rollback()  # Rollback the session to undo the deletion
        flash(
            "Error: This Major cannot be deleted because it is referenced by other records. Please call Network Administrator.",
            "error")
        # app.logger.error(f"Error deleting course: {str(e)}")
        # Redirect back to the admin courses page

    return redirect(url_for('admin.dashboard'))


# -------------------------------------------------------------------------------
@app.route('/admin/dashboard/delete-dept/<int:DepartmentID>', methods=["POST"])
def delete_dept(DepartmentID):
    try:
        # Retrieve the dept with the given DepartmentID from the database
        # major = Major.query.get(MajorID)
        dept = Department.query.get(DepartmentID)
        if dept:
            # If the dept exists, delete it from the database
            db.session.delete(dept)
            db.session.commit()
            flash("Department deleted Successfully.", "Success")
        else:
            flash("Error: Department not found.", "error")
    except Exception as e:
        db.session.rollback()  # Rollback the session to undo the deletion
        flash(
            "Error: This Department cannot be deleted because it is referenced by other records. Please call Network Administrator.",
            "error")
        # app.logger.error(f"Error deleting course: {str(e)}")
        # Redirect back to the admin courses page
    # Redirect back to the admin departments page
    # return redirect(url_for('admin.departments'))
    return redirect(url_for('admin.dashboard'))


# -------------------------------------------------------------------------------
@app.route('/admin/dashboard/delete-course/<int:CourseID>', methods=["POST"])
def delete_course(CourseID):
    try:
        # Retrieve the course with the given CourseID from the database
        course = Course.query.get(CourseID)

        if course:
            # If the major exists, delete it from the database
            db.session.delete(course)
            db.session.commit()
            flash("The desired Course deleted Successfully.", "Success")
        else:
            flash("Error: The desired Course not found.", "error")
    except Exception as e:
        db.session.rollback()  # Rollback the session to undo the deletion
        flash(
            "Error: This course cannot be deleted because it is referenced by other records. Please call Network Administrator.",
            "error")
        # app.logger.error(f"Error deleting course: {str(e)}")
        # Redirect back to the admin courses page
    # return redirect(url_for('admin.courses'))
    return redirect(url_for('admin.dashboard'))


# -------------------------------------------------------------------------------
@app.route('/admin/dashboard/delete-student/<int:StudentID>', methods=["POST"])
def delete_student(StudentID):
    try:
        # Retrieve the student with the given StudentID from the database
        student = Student.query.get(StudentID)
        studentinfo = StudentInfo.query.get(StudentID)
        if student:

            db.session.delete(student)
            db.session.delete(studentinfo)
            db.session.commit()
            flash("Student deleted Successfully.", "Success")
        else:
            flash("Error: Student not found.", "error")
    except Exception as e:
        db.session.rollback()  # Rollback the session to undo the deletion
        flash(
            "Error: This student cannot be deleted because it is referenced by other records. Please call Network Administrator.",
            "error")
        # app.logger.error(f"Error deleting course: {str(e)}")
        # Redirect back to the admin courses page
    # Redirect back to the admin courses page
    # return redirect(url_for('admin.students'))
    return redirect(url_for('admin.dashboard'))


# -------------------------------------------------------------------------------
# SEARCH

@app.route('/admin/dashboard/search_student')
def search_student_page():
    return render_template('admin/search.html')


@app.route('/admin/dashboard/search_student', methods=['POST'])
def search_student():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')

    # Search for the student by first name and last name
    student = Student.query.filter(
        and_(Student.FirstName == firstname.title(), Student.LastName == lastname.title())).first()

    if student:
        # Get related course IDs from the StudentCourse table
        course_ids = [row.CourseID for row in Studentcourse.query.filter(Studentcourse.StudentID == student.StudentID)]

        # Get student info from the StudentInfo table
        student_info = StudentInfo.query.get(student.StudentID)

        # Get the major name from the Majors table based on MajorID
        major = Major.query.get(student.MajorID)
        major_name = major.MajorName if major else None

        # Get course numbers based on course IDs
        course_numbers = []
        course_names = []
        course_units = []
        total_units = 0
        for course_id in course_ids:
            course = Course.query.get(course_id)
            if course:
                course_numbers.append(course.CourseNumber)
                course_names.append(course.CourseDescription)
                course_units.append(course.CourseUnits)
                total_units += course.CourseUnits
            else:
                course_numbers.append(None)

        # Prepare the result to be sent as JSON
        result = {
            "StudentID": student.StudentID,
            "LastName": student.LastName,
            "FirstName": student.FirstName,
            "EnrollmentDate": str(student.EnrollmentDate),  # Convert date to string
            "GraduationDate": str(student.GraduationDate),  # Convert date to string
            "MajorID": student.MajorID,
            "MajorName": major_name,  # MajorName associated with MajorID
            "CourseIDs": course_ids,
            "CourseNumbers": course_numbers,  # CourseNumbers associated with CourseIDs
            "CourseNames": course_names,  # CourseDescription associated with CourseIDs
            "CourseUnits": course_units,  # CourseUnits associated with CourseIDs
            "TotalCourseUnits": total_units,

            "Dob": str(student_info.Dob) if student_info else None,  # Convert date to string
            "Phone": student_info.Phone if student_info else None,
            "Address": student_info.Address if student_info else None,
            "City": student_info.City if student_info else None,
            "State": student_info.State if student_info else None,
            "Zipcode": student_info.Zipcode if student_info else None,
            "Email": student_info.Email if student_info else None,
            "PhotoURL": f"/static/img/{student.StudentID}.jpg",
        }

        return jsonify(result)
    else:
        # If student is not found, return an empty result

        return jsonify({})


# --------------------------------------------------------------------
@app.route('/admin/dashboard/studentinfo', methods=["GET", "POST"])
def studentinfo():
    if request.method == "GET":

        query = text(
            'SELECT majors.MajorID, majors.MajorName FROM majors order by majors.MajorName')
        majors = db.session.execute(query)
        # Convert the query result to a list of tuples
        majors = [(row[0], row[1]) for row in majors]

        query2 = text(
            'SELECT students.StudentID,students.LastName,students.FirstName,students.EnrollmentDate,students.GraduationDate,studentinfo.Dob,studentinfo.Phone,studentinfo.Address,studentinfo.City,studentinfo.State,studentinfo.Zipcode,studentinfo.Email, students.MajorID ,majors.MajorName From  students left outer join  studentinfo  on students.StudentID = studentinfo.StudentID  join   majors ON students.MajorID = majors.MajorID order by students.LastName')
        studentinfo = db.session.execute(query2)
        studentinfo = [
            (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12],
             row[13]) for row
            in studentinfo]
        query3 = text(
            'SELECT students.StudentID,students.LastName,students.FirstName,students.EnrollmentDate,students.GraduationDate,students.MajorID, majors.MajorName FROM students '
            ' join   majors ON students.MajorID = majors.MajorID order by students.LastName')
        students = db.session.execute(query3)
        # Convert the query result to a list of tuples
        students = [(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in students]

        return render_template("admin/studentinfo.html", students=students, majors=majors, studentinfo=studentinfo)
    else:
        LastName = request.form.get('LastName', None)
        FirstName = request.form.get('FirstName', None)
        MajorID = request.form.get('MajorID', None)
        EnrollmentDate = request.form.get('EnrollmentDate')
        GraduationDate = request.form.get('GraduationDate')

        GraduationDate = request.form.get('GraduationDate', None)

        if GraduationDate:
            if GraduationDate == 'None':
                GraduationDate = ''
                print(1)
            else:
                print(2)
                GraduationDate = datetime.strptime(GraduationDate, '%Y-%m-%d')
        else:
            GraduationDate = None

        file = request.files.get('img', None)
        stu = Student(LastName=LastName.title(), FirstName=FirstName.title(), MajorID=MajorID,
                      EnrollmentDate=EnrollmentDate, GraduationDate=GraduationDate)

        db.session.add(stu)
        db.session.commit()
        file.save(f'static/img/{stu.StudentID}.jpg')
        flash("Student added Successfully.", "Success")
        return redirect(url_for("admin.dashboard"))
