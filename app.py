from flask import Flask, render_template, request, redirect, url_for, session
from database import connection, cursor

app = Flask(__name__)
app.secret_key = "employee_management_123"


# -----------------------------
# Login
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT * FROM admin WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))

        admin = cursor.fetchone()

        if admin:

            session["username"] = username

            return redirect(url_for("dashboard"))

        else:

            return render_template(
                "login.html",
                error="Invalid Username or Password"
            )

    return render_template("login.html")

# -----------------------------
# Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login"))

    # Total Employees
    cursor.execute("SELECT COUNT(*) AS total_employee FROM employee")
    result = cursor.fetchone()
    total_employee = result["total_employee"]

    # Total Departments
    cursor.execute("SELECT COUNT(*) AS total_department FROM department")
    result = cursor.fetchone()
    total_department = result["total_department"]

    return render_template(
        "dashboard.html",
        username=session["username"],
        total_employee=total_employee,
        total_department=total_department
    )
# -----------------------------
# Employees
# -----------------------------
@app.route("/employees")
def employees():

    if "username" not in session:
        return redirect(url_for("login"))

    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()

    return render_template(
        "employees.html",
        employees=employees
    )
# -----------------------------
# Add Employee
# -----------------------------
@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        emp_name = request.form["emp_name"]
        gender = request.form["gender"]
        age = int(request.form["age"])
        phone = request.form["phone"]
        email = request.form["email"]
        department = request.form["department"]
        designation = request.form["designation"]
        salary = request.form["salary"]
        joining_date = request.form["joining_date"]

        sql = """
        INSERT INTO employee
        (emp_name, gender, age, phone, email,
        department, designation, salary, joining_date)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
    
            emp_name,
            gender,
            age,
            phone,
            email,
            department,
            designation,
            salary,
            joining_date
        )
        print(request.form)
        print(values)
        cursor.execute(sql, values)
        connection.commit()

        return redirect(url_for("employees"))

    return render_template("add_employee.html")
# -----------------------------
# Edit Employee
# -----------------------------
@app.route("/edit_employee/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        emp_name = request.form["emp_name"]
        gender = request.form["gender"]
        age = request.form["age"]
        phone = request.form["phone"]
        email = request.form["email"]
        department = request.form["department"]
        designation = request.form["designation"]
        salary = request.form["salary"]
        joining_date = request.form["joining_date"]

        sql = """
        UPDATE employee
        SET emp_name=%s,
            gender=%s,
            age=%s,
            phone=%s,
            email=%s,
            department=%s,
            designation=%s,
            salary=%s,
            joining_date=%s
        WHERE emp_id=%s
        """

        values = (
            emp_name,
            gender,
            age,
            phone,
            email,
            department,
            designation,
            salary,
            joining_date,
            id
        )

        cursor.execute(sql, values)
        connection.commit()

        return redirect(url_for("employees"))

    cursor.execute("SELECT * FROM employee WHERE emp_id=%s", (id,))
    employee = cursor.fetchone()

    return render_template("edit_employee.html", employee=employee)
# -----------------------------
# Delete Employee
# -----------------------------
@app.route("/delete_employee/<int:id>")
def delete_employee(id):

    if "username" not in session:
        return redirect(url_for("login"))

    cursor.execute(
        "DELETE FROM employee WHERE emp_id=%s",
        (id,)
    )

    connection.commit()

    return redirect(url_for("employees"))
# -----------------------------
# Attendance
# -----------------------------

@app.route("/attendance")
def attendance():

    if "username" not in session:
        return redirect(url_for("login"))

    cursor.execute("""
        SELECT
            attendance.attendance_id,
            employee.emp_name,
            attendance.attendance_date,
            attendance.status
        FROM attendance
        INNER JOIN employee
        ON attendance.emp_id = employee.emp_id
        ORDER BY attendance.attendance_id DESC
    """)

    attendance_records = cursor.fetchall()

    return render_template(
        "attendance.html",
        attendance=attendance_records
    )


# -----------------------------
# Add Attendance
# -----------------------------

@app.route("/add_attendance", methods=["GET", "POST"])
def add_attendance():

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        emp_id = request.form["emp_id"]
        attendance_date = request.form["attendance_date"]
        status = request.form["status"]

        cursor.execute("""
            INSERT INTO attendance
            (emp_id, attendance_date, status)
            VALUES (%s, %s, %s)
        """, (
            emp_id,
            attendance_date,
            status
        ))

        connection.commit()

        return redirect(url_for("attendance"))

    cursor.execute("""
        SELECT emp_id, emp_name
        FROM employee
        ORDER BY emp_name
    """)

    employees = cursor.fetchall()

    return render_template(
        "add_attendance.html",
        employees=employees
    )


# -----------------------------
# Edit Attendance
# -----------------------------

@app.route("/edit_attendance/<int:id>", methods=["GET", "POST"])
def edit_attendance(id):

    if "username" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        emp_id = request.form["emp_id"]
        attendance_date = request.form["attendance_date"]
        status = request.form["status"]

        cursor.execute("""
            UPDATE attendance
            SET emp_id=%s,
                attendance_date=%s,
                status=%s
            WHERE attendance_id=%s
        """, (
            emp_id,
            attendance_date,
            status,
            id
        ))

        connection.commit()

        return redirect(url_for("attendance"))

    cursor.execute(
        "SELECT * FROM attendance WHERE attendance_id=%s",
        (id,)
    )

    attendance_record = cursor.fetchone()

    cursor.execute("""
        SELECT emp_id, emp_name
        FROM employee
        ORDER BY emp_name
    """)

    employees = cursor.fetchall()

    return render_template(
        "edit_attendance.html",
        attendance=attendance_record,
        employees=employees
    )


# -----------------------------
# Delete Attendance
# -----------------------------

@app.route("/delete_attendance/<int:id>")
def delete_attendance(id):

    if "username" not in session:
        return redirect(url_for("login"))

    cursor.execute(
        "DELETE FROM attendance WHERE attendance_id=%s",
        (id,)
    )

    connection.commit()

    return redirect(url_for("attendance"))

# -----------------------------
# Departments
# -----------------------------
@app.route("/departments")
def departments():

    if "username" not in session:
        return redirect(url_for("login"))

    cursor.execute("SELECT * FROM department")
    departments = cursor.fetchall()

    return render_template(
        "departments.html",
        departments=departments
    )


# -----------------------------
# Payroll
# -----------------------------
@app.route("/payroll")
def payroll():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("payroll.html")


# -----------------------------
# Reports
# -----------------------------
@app.route("/reports")
def reports():

    if "username" not in session:
        return redirect(url_for("login"))

    return render_template("reports.html")


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)