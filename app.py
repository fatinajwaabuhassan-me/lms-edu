from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secretkey"

# In-memory course storage
courses = []

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["username"] = request.form["username"]
        session["role"] = request.form["role"]

        if session["role"] == "educator":
            return redirect("/educator")
        else:
            return redirect("/learner")

    return render_template("login.html")


# ---------------- EDUCATOR ----------------
@app.route("/educator")
def educator():
    if session.get("role") != "educator":
        return redirect("/")
    return render_template("educator.html", courses=courses)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- ADD COURSE ----------------
@app.route("/add_course", methods=["POST"])
def add_course():
    title = request.form["title"]
    courses.append(title)
    return redirect("/educator")


# ---------------- UPDATE COURSE ----------------
@app.route("/update_course/<int:index>", methods=["POST"])
def update_course(index):
    new_title = request.form["new_title"]
    courses[index] = new_title
    return redirect("/educator")


# ---------------- DELETE COURSE ----------------
@app.route("/delete_course/<int:index>")
def delete_course(index):
    courses.pop(index)
    return redirect("/educator")


# ---------------- LEARNER ----------------
@app.route("/learner")
def learner():
    if session.get("role") != "learner":
        return redirect("/")
    return render_template("learner.html", courses=courses)

if __name__ == "__main__":
    app.run(debug=True) 
