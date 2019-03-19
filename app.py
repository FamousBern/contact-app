import os
from flask import Flask, render_template, url_for, flash, session, request, redirect
from flask_login import login_required, UserMixin, current_user, LoginManager, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

#database link
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "message.db"))

app = Flask(__name__)

csrf = CSRFProtect(app)
#database configuration

app.config['SQLALCHEMY_DATABASE_URI'] = database_file
app.config['SECRET_KEY'] = 'BERNARD'
db = SQLAlchemy(app)



#model
class Text_Me(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return "<Body: {}>".format(self.content)

# my form
class ContactForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('submit')


@app.route('/')
def index():
    return render_template('home.html') 


@app.route('/contact', methods=['GET','POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        text = Text_Me(title=form.title.data, content=form.message.data)
        db.session.add(text)
        db.session.commit()
        flash('Message created successifully, thank you for texting.', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)


@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html')


@app.route('/admin', methods=['GET','POST'])
def admin():
    mem = Text_Me.query.all()
    return render_template('admin.html', mem=mem)

@app.route('/delete/<int:id>', methods=['GET','POST'])
def delete(id):
    mem = Text_Me.query.filter_by(id=id).first()
    db.session.delete(mem)
    db.session.commit()
    flash('Message deleted', 'danger')
    return redirect(url_for('admin')) 


if __name__ == '__main__':
    app.run(debug=True)