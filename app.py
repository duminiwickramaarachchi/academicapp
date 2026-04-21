from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

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

        # plain-text password check
        cursor.execute("""
            SELECT * FROM user
            WHERE username=? AND password=? AND role='admin'
        """, (username, password))

        user = cursor.fetchone()
        conn.close()

        if user:
            return "Admin login successful!"
        else:
            return "Invalid username or password"

    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)