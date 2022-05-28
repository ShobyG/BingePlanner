from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from flask_login import current_user, login_user, login_required, logout_user
from wtforms.validators import ValidationError

from calender_event import CalenderEvent
from imdb import find_titles, find_id
from imdb_practice import find_specific_titles
from wiki import find_births
from models import db, login, UserModel
from datetime import date


class loginForm(FlaskForm):
    email = StringField(label="Enter email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Enter password", validators=[DataRequired(), Length(min=6, max=16)])
    submit = SubmitField(label="Login")


class Search(FlaskForm):
    search_titles = StringField(label="Please enter the Title you are looking for", validators=[DataRequired()])
    submit = SubmitField(label="Search")
    choose = SubmitField(label="Approve")


class Advanced_Search(FlaskForm):
    search_titles = StringField(label="Please enter the Title you are looking for", validators=[DataRequired()])
    input_ID = StringField(label="Please enter the IMDB ID to pick your movie", validators=[DataRequired()])

    submit = SubmitField(label="Submit")
    # choose = SubmitField(label="Approve")


class MovieEventForm(FlaskForm):
    """ form to create movie event"""
    event_name = StringField(label="movie name", validators=[DataRequired()])
    length = IntegerField(label="movie length", validators=[DataRequired()])
    start_date = DateField(label="watch movie on", default=date.today(), validators=[DataRequired()])
    start_time = TimeField("Start")
    add_event = SubmitField(label="Add event")


class Input(FlaskForm):
    input_time = IntegerField(label="Please input the amount of time you wish to invest", validators=[DataRequired()])
    # birthday = DateField(label="Please enter when you would like to start", default=date.today(), validators=[DataRequired()])
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


# @app.route('/search', methods=["POST", "GET"])
# def search_title():
#     form = Search()
#     aForm = Advanced_Search()
#
    # if form.validate_on_submit():
    #     if aForm.validate_on_submit():
#
#             if current_user.is_authenticated:
#                 if request.method == "POST":
#                     title = request.form["search_titles"]
#                     imdbID = request.form["input_ID"]
#                     # digits = request.form["digit"]
#                     return render_template("search2.html", form=aForm, myData=find_specific_titles(title, imdbID))
#                 elif request.method == "GET":
#                     title = request.form["search_titles"]
#                     imdbID = request.form["input_ID"]
#
#                     return render_template("display_selection.html", form=aForm, myData=find_specific_titles(title, imdbID))
#             return redirect("/")
#         return render_template("home.html", form=aForm)
#     return redirect("/display")


@app.route('/search', methods=["POST", "GET"])
def search_title():
    form = Search()
    aForm = Advanced_Search()
    # find_specific_titles(title, imdbID)

    if form.submit.data and form.validate_on_submit():
        if current_user.is_authenticated:
            if request.method == "POST":
                title = request.form["search_titles"]
                return render_template("search.html", form=form, aForm=aForm, myData=find_titles(title))
    else:
        flash(f"request.errors")

    if aForm.submit.data and aForm.validate_on_submit():
        if current_user.is_authenticated:
            if request.method == "POST":
                title = request.form["search_titles"]
                id = request.form["input_ID"]
                return render_template("search.html", form=form, aForm=aForm, myData=find_specific_titles(title, id))


            # elif request.method == "GET":
            #     return render_template("display_selection.html", aForm=aForm)

        # return redirect("/")

    return render_template("search.html", form=form)

    # if form.submit.data and form.validate_on_submit():


@app.route("/display", methods=["POST", "GET"])
def display_choice():
    # form = Input()
    form = Search()
    aForm = Advanced_Search()
    # if current_user.is_authenticated:
    #     return render_template("display_selection.html", form=form)
    if aForm.validate_on_submit():
        if current_user.is_authenticated:
            if request.method == "POST":
                title = request.form["search_titles"]
                id = request.form["input_ID"]
                # title = request.form["moreinfo"]
                # digits = request.form["digit"]
                return render_template("search2.html", form=aForm, myData=find_titles(title, id))
                # return render_template("display_selection.html", form=form, myData=search_title())
            elif request.method == "GET":
                return render_template("display_selection.html", form=aForm)
        return "/display"
    return render_template("home.html", form=aForm)


@app.route('/movie_event', methods=["POST", "GET"])
def movie_event_page():
    form = MovieEventForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            if request.method == "POST":
                event_name = request.form["event_name"]
                length = request.form["length"]
                start_date = request.form["start_date"]
                start_time = request.form["start_time"]
                ce = CalenderEvent([], event_name, start_date, start_time, length)
                events = ce.events
                return render_template("calendar.html", events=events)
            if request.method == "GET":
                return render_template("movie_event.html", form=form)
    return render_template("movie_event.html", form=form)

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