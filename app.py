from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

# __name__: the name of the application
app = Flask(__name__)
# 3 slashes: relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# initialize the database with the settings from app
db = SQLAlchemy(app)

# define a model for our database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # representation method: defines how the object is represented as a string
    # printing an instance of Todo will return a string in the format <Task id>
    def __repr__(self):
        return '<Task %r>' % self.id
    
with app.app_context():
    db.create_all()


# define a get route
@app.route('/', methods=['GET', 'POST'])
def index():
    if (request.method == "POST"):
        # get the task content from the form data and create a new Todo object
        task_content = request.form['task']
        # create a new instance of Todo
        new_task = Todo(content = task_content)
    
        try:
            # add the new task to the database and commit the changes
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem adding the task'

    else:
        # get all tasks from the database
        tasks = Todo.query.order_by(Todo.date_created).all()
        # return the template with context
        return render_template('index.html', tasks = tasks)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def updateTask(id):
    # get the task based on the id
    taskToUpdate = Todo.query.get_or_404(id)

    if (request.method == 'POST'):
        updatedContent = request.form['task']
        taskToUpdate.content = updatedContent
        taskToUpdate.date_created = datetime.now(timezone.utc)

        try:
            db.session.commit()
        except:
            return 'There was a problem updating the task'
        return redirect('/')
    
    else:
        return render_template('update.html', task = taskToUpdate)


# id is passed into the function
@app.route('/delete/<int:id>')
def deleteTask(id):
    # get the task based on the id
    taskToDelete = Todo.query.get_or_404(id)

    try:
        # delete the task from the database and commit the changes
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the task'


# error popup on the web page
if (__name__ == "__main__"):
    app.run(debug=True)