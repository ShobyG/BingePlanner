from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from flask_login import current_user, login_user, login_required, logout_user
from wtforms.validators import ValidationError

from imdb import find_titles
from wiki import find_births
from models import db, login, UserModel
from datetime import date


class loginForm(FlaskForm):
    email = StringField(label="Enter email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Enter password", validators=[DataRequired(), Length(min=6, max=16)])
    submit = SubmitField(label="Login")


# class Search(FlaskForm):
#     digit = IntegerField(label="Number of results", default=10, validators=[DataRequired(), NumberRange(min=1, max=20)])
#     submit = SubmitField(label="Search")
#     birthday = DateField(label="Enter your birthday", default=date.today(), validators=[DataRequired()])

    # def validate_birthday(self, field):
    #     if field.data > date.today():
    #         flash("Choose a past or present date")
    #         raise ValidationError("Choose a past or present date")

class Search(FlaskForm):
    search_titles = StringField(label="Please enter the Title you are looking for", validators=[DataRequired()])
    # digit = IntegerField(label="Number of results", default=10, validators=[DataRequired(), NumberRange(min=1, max=20)])
    submit = SubmitField(label="Search")




app = Flask(__name__)
app.secret_key = "a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)


def addUser(email, password):
    # check if email or username exits
    user = UserModel()
    user.set_password(password)
    user.email = email
    db.session.add(user)
    db.session.commit()


@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(email="vinz_klortho@msn.com").first()
    if user is None:
        addUser("vinz_klortho@msn.com", "reek42")


# @app.route('/birthday', methods=["POST", "GET"])
# def same_birthday():
#     form = Search()
#     if form.validate_on_submit():
#         if current_user.is_authenticated:
#             if request.method == "POST":
#                 birthday = request.form["birthday"]
#                 birthday = birthday.split("-")
#                 digits = request.form["digit"]
#                 return render_template("search.html", form=form, myData=find_births(f"{birthday[1]}/{birthday[2]}",
#                                                                                     birthday[0], digits))
#             elif request.method == "GET":
#                 return render_template("home.html", form=form)
#         return redirect("/")
#     return render_template("home.html", form=form)

@app.route('/search', methods=["POST", "GET"])
def search_title():
    form = Search()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            if request.method == "POST":
                title = request.form["search_titles"]
                # digits = request.form["digit"]
                return render_template("search.html", form=form, myData=find_titles(title))
            elif request.method == "GET":
                return render_template("home.html", form=form)
        return redirect("/")
    return render_template("home.html", form=form)


@app.route("/")
def root():
    form = Search()
    if current_user.is_authenticated:
        return render_template("home.html", form=form)
    return redirect("/login")


@app.route('/home')
def home():
    return redirect("/search")


@app.route('/login', methods=["POST", "GET"])
def login():
    form = loginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            pw = request.form["password"]
            user = UserModel.query.filter_by(email=email).first()
            if user is not None and user.check_password(pw):
                login_user(user)
                flash(f"Welcome back {email}. Logged in successfully", "info")
                # flash("Please input date and range of results", "info")
                return redirect('/home')
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
