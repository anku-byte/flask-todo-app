from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Render-safe SQLite path
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.id}>"

# Create DB tables at startup
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_content = request.form["content"]
        new_task = Todo(content=task_content)
        db.session.add(new_task)
        db.session.commit()
        return redirect("/")

    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    task = Todo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]
        db.session.commit()
        return redirect("/")

    return render_template("update.html", task=task)

# IMPORTANT: DO NOT run app here (Gunicorn will)
if __name__ == "__main__":
    pass
