from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/', static_folder="public", template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasklist-python.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), default="New Task")
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
    

# class Task(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.String(100))
#     done = db.Column(db.Boolean)

@app.route('/')
def task_list():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/add-task", methods=[ "POST" ])
def add_task():
    body = request.get_json()
    content = body["content"]
    if not content:
        return "specify a task"

    new_task = Task(content=content)
    db.session.add(new_task)
    db.session.commit()
    return "created task"

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return "task id doesn't exist"
    
    db.session.delete(task)
    db.session.commit()
    return "deleted task"

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return "task id doesn't exist"

    task.done = not task.done
    db.session.commit()
    return "changed task"


if __name__ == "__main__":
    db.create_all()    
    app.run(debug=True)