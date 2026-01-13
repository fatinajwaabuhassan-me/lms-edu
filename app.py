from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secretkey"

# TEMP in-memory data (for deployment stability)
courses = []

# -------------------------
# LOGIN PAGE
# -------------------------
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


# -------------------------
# EDUCATOR PAGE
# -------------------------
@app.route("/educator")
def educator():
    if session.get("role") != "educator":
        return redirect("/")
    return render_template("educator.html", courses=courses)


# -------------------------
# ADD COURSE
# -------------------------
@app.route("/add_course", methods=["POST"])
def add_course():
    if session.get("role") != "educator":
        return redirect("/")

    title = request.form["title"]
    courses.append(title)
    return redirect("/educator")


# -------------------------
# DELETE COURSE
# -------------------------
@app.route("/delete_course/<int:index>")
def delete_course(index):
    if session.get("role") != "educator":
        return redirect("/")

    if index < len(courses):
        courses.pop(index)
    return redirect("/educator")


# -------------------------
# LEARNER PAGE
# -------------------------
@app.route("/learner")
def learner():
    if session.get("role") != "learner":
        return redirect("/")
    return render_template("learner.html", courses=courses)
