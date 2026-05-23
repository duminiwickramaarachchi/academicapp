from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# connect to database
def get_db():
    return sqlite3.connect("academic.db")


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, role FROM user
            WHERE username=? AND password=?
        """, (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[1]

            if user[1] == "admin":
                return redirect(url_for("admin_dashboard"))

            elif user[1] == "lecturer":
                return redirect(url_for("lecturer_dashboard"))

            elif user[1] == "student":
                return redirect(url_for("student_dashboard"))

        return "Invalid username or password"

    return render_template("login.html")



from flask import redirect, url_for

# ADMIN DASHBOARD
@app.route("/admin")
def admin_dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # USERS (MUST BE FIRST OR AT LEAST BEFORE RETURN)
    cursor.execute("SELECT id, username, role FROM user")
    users = cursor.fetchall()

    # SUBJECTS
    cursor.execute("""
        SELECT subjects.id, subjects.name, user.username
        FROM subjects
        LEFT JOIN user ON subjects.lecturer_id = user.id
    """)
    subjects = cursor.fetchall()

    # ENROLLMENTS
    cursor.execute("""
        SELECT enrollments.subject_id, user.id, user.username
        FROM enrollments
        JOIN user ON enrollments.student_id = user.id
    """)
    enrollments = cursor.fetchall()

    conn.close()

    return render_template(
        "admin.html",
        users=users,
        subjects=subjects,
        enrollments=enrollments
    )


# CREATE USER
@app.route("/create_user", methods=["POST"])
def create_user():
    try:
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO user (username, password, role)
            VALUES (?, ?, ?)
        """, (username, password, role))

        conn.commit()
        conn.close()

        return redirect(url_for('admin_dashboard'))

    except Exception as e:
        return f"CREATE USER ERROR: {e}"

    finally:
        if conn:
            conn.close()

# DELETE USER
@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):

    conn = None

    try:
        conn = get_db()
        cursor = conn.cursor()

        # delete enrollments first
        cursor.execute("""
            DELETE FROM enrollments
            WHERE student_id=?
        """, (user_id,))

        # remove lecturer from subjects
        cursor.execute("""
            UPDATE subjects
            SET lecturer_id=NULL
            WHERE lecturer_id=?
        """, (user_id,))

        # delete user
        cursor.execute("""
            DELETE FROM user
            WHERE id=?
        """, (user_id,))

        conn.commit()

        return redirect(url_for('admin_dashboard'))

    except Exception as e:
        return f"DELETE USER ERROR: {e}"

    finally:
        if conn:
            conn.close()

# Create Subject
@app.route("/create_subject", methods=["POST"])
def create_subject():
    try:
        name = request.form["name"]
        lecturer_id = request.form["lecturer_id"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO subjects (name, lecturer_id)
            VALUES (?, ?)
        """, (name, lecturer_id))

        conn.commit()
        conn.close()

        return redirect(url_for('admin_dashboard'))

    except Exception as e:
        return f"CREATE SUBJECT ERROR: {e}"
    
    finally:
        if conn:
            conn.close()

# Enroll Student
@app.route("/enroll_student", methods=["POST"])
def enroll_student():
    conn = None

    try:
        student_id = request.form["student_id"]
        subject_id = request.form["subject_id"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO enrollments (student_id, subject_id)
            VALUES (?, ?)
        """, (student_id, subject_id))

        conn.commit()

        return redirect(url_for('admin_dashboard'))

    except Exception as e:
        return f"ENROLL ERROR: {e}"

    finally:
        if conn:
            conn.close()


# Change Lecturer
@app.route("/change_lecturer", methods=["POST"])
def change_lecturer():
    subject_id = request.form["subject_id"]
    lecturer_id = request.form["lecturer_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE subjects
        SET lecturer_id=?
        WHERE id=?
    """, (lecturer_id, subject_id))

    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))



#Remove Student
@app.route("/remove_student/<int:student_id>/<int:subject_id>")
def remove_student(student_id, subject_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM enrollments
        WHERE student_id=? AND subject_id=?
    """, (student_id, subject_id))

    conn.commit()
    conn.close()

    return redirect(url_for('admin_dashboard'))



@app.route("/lecturer_dashboard")
def lecturer_dashboard():
    if "role" not in session or session["role"] != "lecturer":
        return redirect(url_for("login"))

    lecturer_id = session["user_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM subjects
        WHERE lecturer_id=?
    """, (lecturer_id,))
    subjects = cursor.fetchall()

    cursor.execute("""
        SELECT enrollments.subject_id,
            enrollments.student_id,
            user.username,
            enrollments.marks
        FROM enrollments
        JOIN user ON enrollments.student_id = user.id
    """)
    enrollments = cursor.fetchall()

    cursor.execute("""
        SELECT subject_id, AVG(marks)
        FROM enrollments
        GROUP BY subject_id
    """)
    averages = cursor.fetchall()

    conn.close()

    return render_template(
        "lecturer.html",
        subjects=subjects,
        enrollments=enrollments,
        averages=averages
    )


@app.route("/save_marks", methods=["POST"])
def save_marks():

    student_id = request.form["student_id"]
    subject_id = request.form["subject_id"]
    marks = request.form["marks"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE enrollments
        SET marks=?
        WHERE student_id=? AND subject_id=?
    """, (marks, student_id, subject_id))

    conn.commit()
    conn.close()

    return redirect(url_for("lecturer_dashboard"))


@app.route("/student_dashboard")
def student_dashboard():
    if "role" not in session or session["role"] != "student":
        return redirect(url_for("login"))

    student_id = session["user_id"]

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT subjects.name, enrollments.marks
        FROM enrollments
        JOIN subjects ON enrollments.subject_id = subjects.id
        WHERE enrollments.student_id=?
    """, (student_id,))

    data = cursor.fetchall()

    cursor.execute("""
        SELECT AVG(marks)
        FROM enrollments
        WHERE student_id=?
    """, (student_id,))

    avg_marks = cursor.fetchone()[0]


    conn.close()

    return render_template(
    "student.html",
    data=data,
    avg_marks=avg_marks
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

#if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)