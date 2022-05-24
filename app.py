from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, InputRequired, NumberRange
from wiki import find_titles
from flask_login import current_user, login_user, login_required, logout_user
from models2 import db2, login2, UserModel2
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

events = [
    {
        'title' : 'Tutorial',
        'start' : '2022-05-18',
        'end': '',
        'url': ''
    },
    {
        'title' : 'Tutorial',
        'start' : '2022-05-19',
        'end': '',
        'url': ''
    },
    ] 
    
app.secret_key="a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db2.init_app(app)
login2.init_app(app)

def addUser2(username, password):
    user2=UserModel2()
    user2.set_password(password)
    user2.username = username
    db2.session.add(user2)
    db2.session.commit()
    return user2

@app.before_first_request
def create_table():
    db2.create_all()
    user2 = UserModel2.query.filter_by(username = 'test').first()
    if user2 is None:
        addUser2('test', 'qwerty')
        
class hwLoginForm(FlaskForm):
    username=StringField(label="Username",validators=[DataRequired(), Length(min=6,max=20)])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Login")

class hwRegForm(FlaskForm):
    username=StringField(label="Username",validators=[DataRequired(), Length(min=6,max=20)])
    password=PasswordField(label="Enter password",validators=[DataRequired(), Length(min=6,max=16)])
    submit=SubmitField(label="Register")

class searchForm(FlaskForm):
    search_text=StringField(validators=[DataRequired()])
    submit=SubmitField(label="Search")

@app.route("/search",methods=['GET','POST'])
@login_required
def search():
    form = searchForm()
    if form.validate_on_submit():
        if request.method == "POST":
            title = request.form["search_text"]
            return render_template("search.html", myData=find_titles(title),form=form)
        else:
            return render_template("search.html", form=form)
    else:
        print(form.errors)
    return render_template("search.html",form=form)

@app.route("/home",methods=['GET','POST'])
def home():
    return render_template("index.html")

@app.route("/")
def redirectToLogin():
    return redirect("/home")

@app.route("/login",methods=['GET','POST'])
def login():
    form=hwLoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username=request.form["username"]
            pw=request.form["password"]
            user = UserModel2.query.filter_by(username = username).first()
            if user is not None: 
                if user.check_password(pw):
                    login_user(user)
                    print(f"logging in user: {user}")
                    return redirect('/search')
                else:
                    print(form.errors)
                    return render_template("login.html", form=form, fail="failed")
            else:
                print(form.errors)
                return render_template("login.html", form=form, fail="failed")
    else:
        print(form.errors)
    return render_template("login.html",form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/register.html',methods=['GET','POST'])
def register():
    form=hwRegForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username=request.form["username"]
            pw=request.form["password"]
            user = UserModel2.query.filter_by(username = username).first()
            print(f"user: {user}")
            if user is None:
                newuser = addUser2(username, pw)
                print(f"adding user: {newuser}")
                login_user(newuser)
                print(f"logged in user: {newuser}")
                return redirect('/search')
            else:
                print(f"else user is not none: {user}")
                return redirect('/register')
        else:
            print("GET request")
    else:
        print(form.errors)
    return render_template("register.html",form=form)

@app.route('/calendar')
def calendar():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        url = request.form['url']
        if end == '':
            end=start
        events.append({
            'title' : title,
            'start' : start,
            'end': end,
            'url': url
        },
        )
    return render_template("calendar.html", events=events)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        url = request.form['url']
        if end == '':
            end=start
        events.append({
            'title' : title,
            'start' : start,
            'end': end,
            'url': url
        },
        )
    return render_template("calendar.html", events=events)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
