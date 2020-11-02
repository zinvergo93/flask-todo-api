from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Todo(db.Model):
    __tablename = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean)

    def __init__(self, title, done):
        self.title = title
        self.done = done

class TodoSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "done")

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

@app.route("/")
def hello():
    return "Hello, world!"

@app.route('/api/create-todo', methods= ['POST'])
def add_todo():
    title = request.json['title']
    done = request.json['done']

    new_todo = Todo(title, done)
    db.session.add(new_todo)
    db.session.commit()
    todo = Todo.query.get(new_todo.id)
    return todo_schema.jsonify(todo)

@app.route('/api/get-all-todos', methods=['GET'])
def get_todos():
    all_todos = Todo.query.all()
    result = todos_schema.dump(all_todos)
    return jsonify(result)

@app.route('/api/edit-todo/<id>', methods=['PATCH'])
def edit_todo(id):
    todo = Todo.query.get(id)
    new_done = request.json['done']
    todo.done = new_done
    db.session.commit()
    return todo_schema.jsonify(todo)

@app.route('/api/delete-todo/<id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify('TODO deleted')

if __name__ == "__main__":
    app.debug = True
    app.run()