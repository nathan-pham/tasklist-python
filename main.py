from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasklist-python.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

db.create_all()

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Text)
    content = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return 'Task(content=%s)' % self.content        

@app.route('/')
def task_list():
    tasks = Task.query.all()
    return render_template("list.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)