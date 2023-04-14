from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy() 
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///esse.db"
db.init_app(app)
import os
from werkzeug.utils import secure_filename 
UPLOAD_FOLDER ='./static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from sqlalchemy import desc
from flask import Flask, redirect, url_for

class Text(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=True)
    content = db.Column(db.String(10000), nullable = True)

   

    def __init__(self, content,number):
        self.content = content
        self.number = number

@app.route("/add-essy", methods = ['GET', 'POST'])
def addessy():
    if request.method == "GET":
        return   render_template('addessy.html')
    else:
        replacements = [('!', ''), ('?', ''), ('.', ''), (',', '')]
        content = request.form['content']
        content2 = request.form['content']

        for char, replacement in replacements:
            if char in content2:
                content2 = content2.replace(char, replacement)
        

        a = content2.split()

        print(len(a))
        
        number = len(a)
        
        new_text = Text(content, number)
        db.session.add(new_text)
        db.session.commit()
        return redirect(url_for('text'))

@app.route("/")
def text():
    text = Text.query.order_by(desc(Text.id))
    return render_template('essy.html', text=text)
 
@app.route('/deletenote/<int:id>')
def deletenote(id):
    text = Text.query.get(id)
    db.session.delete(text)
    db.session.commit()
    return redirect(url_for('text'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)

