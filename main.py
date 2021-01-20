from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='/', static_folder="public", template_folder="templates")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasklist-python.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    done = db.Column(db.Text)
    content = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return 'Task(content=%s)' % self.content    

db.create_all()    

@app.route('/')
def task_list():
    tasks = Task.query.all()
    return render_template("index.html", tasks=tasks)

if __name__ == "__main__":
    app.run(debug=True)