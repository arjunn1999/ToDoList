from flask import Flask,render_template,redirect
from flask import request
from datetime import datetime
import os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)
class Todo(db.Model):
    sno  = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(200),nullable=False)
    description = db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    def __repr__(self):
        return f"{self.sno} - {self.title}"
@app.route('/',methods=['GET'])
def hello_world():
    alltodo=Todo.query.all()
    return render_template("index.html",alltodo=alltodo)
@app.route("/insert",methods=["POST"])
def insert():
    try:

        title=request.form['title']
        description=request.form['desc']
        todo = Todo(title=title,description=description)
        db.session.add(todo)
        db.session.commit()
        alltodo=Todo.query.all()
    except :
        return redirect("/")
    return redirect("/")
@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method=="GET":
        return render_template("update.html",todo=todo)
    else:
        todo.title=request.form['title']
        todo.description=request.form['desc']
        db.session.commit()
        return redirect("/")
if __name__ == '__main__':
    app.run(debug=True)