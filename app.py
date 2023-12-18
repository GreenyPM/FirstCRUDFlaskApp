from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#Classes are stetups for SQlite Databases
class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.id}>'
    #the function above returns the Id of the class above.

# Move the create_all() call into a function


@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # this pulls data from the form on the html that has the 'content' tag or id
        new_task = todo(content = task_content) # this then sets the content section of test.db to the data previously scalped from the form.

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task, please contact the admin or try again later.'
    else:
        tasks = todo.query.order_by(todo.dateCreated).all()
        return render_template("index.html", noted_tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting your task at the time. Please try again later."


@app.route('/update/<int:id>', methods = ['POST','GET'])
def update(id):
    task = todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with your updated task, try again later.'

    else:
        return render_template('update.html', task = task)



#To run from a ternimal simply type in python app.py or python3 app.py

if __name__ == "__main__":
    app.run(debug=True)