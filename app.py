from flask import Flask, render_template, request, redirect, session
import pyodbc

app = Flask(__name__)
app.secret_key = "secretkey"

# Azure SQL connection
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=your-server-name.database.windows.net;"
    "DATABASE=lmsdb;"
    "UID=adminuser;"
    "PWD=YourPassword;"
    "Encrypt=yes;"
)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        role = request.form["role"]

        session["username"] = username
        session["role"] = role

        if role == "educator":
            return redirect("/educator")
        else:
            return redirect("/learner")

    return render_template("login.html")

@app.route("/educator")
def educator():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return render_template("educator.html", courses=courses)

@app.route("/add_course", methods=["POST"])
def add_course():
    title = request.form["title"]
    cursor = conn.cursor()
    cursor.execute("INSERT INTO courses (title) VALUES (?)", title)
    conn.commit()
    return redirect("/educator")

@app.route("/learner")
def learner():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    return render_template("learner.html", courses=courses)

if __name__ == "__main__":
    app.run(debug=True)
