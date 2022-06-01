from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, DateField, TimeField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange
from flask_login import current_user, login_user, login_required, logout_user
from wtforms.validators import ValidationError
from datetime import date, datetime
import json
import os
from wiki import find_titles, find_id, find_episodes, find_season_episodes
from series_info import SeriesInfo
from models import db, login, UserModel, EventModel

from calendar_planner import CalenderMovieEvent, CalenderSeriesEvent
from event_planner import EventPlanner

class Username:
    """ to store the username """
    def __init__(self):
        self.__username = ""

    def set_username(self, username):
        self.__username = username

    def get_username(self):
        return self.__username


class HwLoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField(label="Enter password", validators=[DataRequired(), Length(min=6, max=16)])
    submit = SubmitField(label="Login")


class HwRegForm(FlaskForm):
    email = StringField(label="Enter email", validators=[DataRequired(), Email()])

    def validate_email(self, field):
        user = UserModel.query.filter_by(email=f"{field.data}").first()
        if user is not None:
            flash(f"{field.data} already in use.Choose a different mail id ")
            raise ValidationError(f"{field.data} already in use.Choose a different mail id ")

    username = StringField(label="Enter username",
                           validators=[DataRequired(), Length(min=6, max=20)])

    def validate_username(self, field):
        user = UserModel.query.filter_by(username=f"{field.data}").first()
        if user is not None:
            flash(f"{field.data} taken.Choose a different name")
            raise ValidationError(f"{field.data} taken.Choose a different name")

    password = PasswordField(label="Enter password", validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField(label='Confirm Password', validators=[DataRequired(), EqualTo('password', message='Both password fields must be equal!')])
    submit = SubmitField(label="Signup")


class searchForm(FlaskForm):
    search_text=StringField(validators=[DataRequired()])
    submit=SubmitField(label="Search")

class titleForm(FlaskForm):
    title_name = StringField(label="title name", render_kw={'readonly': True})
    title_plot = StringField(label="plot", render_kw={'readonly': True})
    title_image = FileField()  
    title_seasons = StringField(label="seasons")    
    title_rating = StringField(label="rating")
    # season_btn = SubmitField(label = "Season X")
    season_runtime = StringField(label="season runtime:")
        
class MovieEventForm(FlaskForm):
    """ form to create movie event"""
    event_name = StringField(label="movie name", validators=[DataRequired()])
    length = IntegerField(label="movie length", validators=[DataRequired()])
    start_date = DateField(label="watch movie on", default=date.today(), validators=[DataRequired()])

    def validate_start_date(self, field):
        if field.data < date.today():
            flash("Choose a future date to plan")
            raise ValidationError("Choose a future date to plan")
    start_time = TimeField("Start")

    def validate_start_time(self, field):
        user_time = datetime.strptime(str(field.data), '%H:%M:%S')  # convert to datetime type
        now = (str(datetime.now()).split(" ")[1]).split(".")[0]  # convert to datetime equivalent to user_time
        now = datetime.strptime(str(now), '%H:%M:%S')
        if user_time < now:
            flash("Cannot choose a passed time")
            raise ValidationError("Cannot choose a passed time")
    add_event = SubmitField(label="Add event")


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SeriesEventForm(FlaskForm):
    """ Form to create series event"""
    series_name = StringField(label="movie name", validators=[DataRequired()])
    length = IntegerField(label="movie length", validators=[DataRequired()])
    days = SelectMultipleField('Watch Days', choices=[
                                       ('0', 'Monday'),
                                       ('1', 'Tuesday'),
                                       ('2', 'Wednesday'),
                                       ('3', 'Thursday'),
                                       ('4', 'Friday'),
                                       ('5', 'Saturday'),
                                       ('6', 'Sunday')
                                   ])
    monday = IntegerField(label='Monday', default=0, validators=[NumberRange(min=0, max=24)])
    tuesday = IntegerField(label='Tuesday', default=0, validators=[NumberRange(min=0, max=24)])
    wednesday = IntegerField(label='Wednesday', default=0, validators=[NumberRange(min=0, max=24)])
    thursday = IntegerField(label='Thursday', default=0, validators=[NumberRange(min=0, max=24)])
    friday = IntegerField(label='Friday', default=0, validators=[NumberRange(min=0, max=24)])
    saturday = IntegerField(label='Saturday', default=0, validators=[NumberRange(min=0, max=24)])
    sunday = IntegerField(label='Sunday', default=0, validators=[NumberRange(min=0, max=24)])
    add_event = SubmitField(label="Add event")


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your secret key'
app.secret_key = "a secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login.init_app(app)
un = Username()


def add_user(email, username, password):
    # check if email or username exits
    user = UserModel()
    user.set_password(password)
    user.username = username
    user.email = email
    db.session.add(user)
    db.session.commit()


def add_event(username, events):
    # add user events json to database
    ue = EventModel()
    ue.username = username
    ue.events = events
    db.session.add(ue)
    db.session.commit()


def del_event(username):
    EventModel.query.filter_by(username=username).delete()


@app.before_first_request
def create_table():
    db.create_all()
    user = UserModel.query.filter_by(username="test123").first()
    if user is None:
        add_user("test@testuser.com", "test123", "test12345")


@app.route("/search", methods=['GET', 'POST'])
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

@app.route("/<imdb_id>", methods=['GET', 'POST'])
def search_by_imdb_id(imdb_id):
    form = titleForm()
    myData = SeriesInfo(imdb_id)
    global user_choices
    user_choices = {}
    
    if request.method == "POST":
        btn_txt = request.form["season_b"]
        split = btn_txt.split("-",1)
        season = int(split[1])
        print(f"parsed season: {season}")
        user_choices["season"] = season
        season_runtime = myData.series_runtime_totals[season]
        user_choices["season_runtime"] = season_runtime
        title = myData.series_title + " (Season " + str(season) + ")"
        user_choices["title"] = title
        print(f"USER CHOICE DICT: {user_choices}")
        return redirect("/series_event")
    
    return render_template("title.html", myData=myData, form=form)

@app.route("/home",methods=['GET','POST'])
def home():
    return render_template("index.html")


@app.route("/")
def redirectToLogin():
    return redirect("/home")


@app.route("/login",methods=['GET','POST'])
def login():
    form = HwLoginForm()
    if form.validate_on_submit():
        if request.method == "POST":
            username = request.form["username"]
            pw = request.form["password"]
            user = UserModel.query.filter_by(username=username).first()
            if user is not None: 
                if user.check_password(pw):
                    login_user(user)
                    un.set_username(username)
                    flash(f"Welcome back {username}. Logged in successfully", "info")
                    return redirect('/search')
                else:
                    flash(form.errors)
                    return render_template("login.html", form=form, fail="failed")
            else:
                flash(form.errors)
                return render_template("login.html", form=form, fail="failed")
    else:
        flash(form.errors)
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect('/login')


@app.route('/base')
def base():
    return render_template("base.html")


@app.route('/index.html')
def index():
    return render_template("index.html")


@app.route('/register.html', methods=['GET','POST'])
def register():
    form = HwRegForm()
    if form.validate_on_submit():
        if request.method == "POST":
            email = request.form["email"]
            pw = request.form["password"]
            username = request.form["username"]
            user = UserModel.query.filter_by(email=email).first()
            if user is not None:
                flash("Existing user... please log in!")
                return redirect('/login')
            else:
                add_user(email, username, pw)
                flash(f"Registered successfully... Logging in as {username}!")
                user = UserModel.query.filter_by(username=username).first()
                login_user(user)
                return redirect('/home')
    return render_template('register.html', form=form)


@app.route('/series_event', methods=["POST", "GET"])
def series_event_page():
    form = SeriesEventForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            if request.method == "POST":
                form.series_name.data = user_choices['title']
                form.length.data = user_choices ['season_runtime']
                series_name = request.form["series_name"]
                length = request.form["length"]
                monday = request.form["monday"]
                tuesday = request.form["tuesday"]
                wednesday = request.form["wednesday"]
                thursday = request.form["thursday"]
                friday = request.form["friday"]
                saturday = request.form["saturday"]
                sunday = request.form["sunday"]
                watch_hours = [int(monday), int(tuesday), int(wednesday), int(thursday), int(friday), int(saturday), int(sunday)]
                days = request.form.getlist(key="days")
                days_lst = [0, 0, 0, 0, 0, 0, 0]
                for i in range(7):
                    if str(i) in days:
                        days_lst[i] = 1
                ep = EventPlanner(series_name, days_lst, watch_hours, int(length))
                dates_lst = ep.date_generator()
                user_event = EventModel.query.filter_by(username=un.get_username()).first()
                if user_event is not None:
                    events = create_event_list()
                    del_event(un.get_username())
                else:
                    events = []

                cse = CalenderSeriesEvent(events, series_name, dates_lst)
                events = cse.events
                create_json_file(un.get_username(), events)
                return redirect("/calendar")
            if request.method == "GET":
                return render_template("series_event.html", form=form)
    return render_template("series_event.html", form=form)


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
                user_event = EventModel.query.filter_by(username=un.get_username()).first()
                if user_event is not None:
                    events = create_event_list()
                    del_event(un.get_username())
                else:
                    events = []
                ce = CalenderMovieEvent(events, event_name, start_date, start_time, length)
                events = ce.events
                create_json_file(un.get_username(), events)
                return redirect("/calendar")
            if request.method == "GET":
                return render_template("movie_event.html", form=form)
    return render_template("movie_event.html", form=form)


@app.route('/calendar', methods=["POST", "GET"])
def user_calendar():
    events = create_event_list()
    return render_template("calendar.html", events=events)


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def write_to_file(blob_data, name):
    # Convert binary data to proper format and write it the pickle file
    with open(f'{name}.json', 'wb') as file:
        file.write(blob_data)


def create_json_file(username, events):
    """ converts the events list to json"""
    with open(f"{username}.json", "w") as write_file:
        json.dump(events, write_file)
    json_binary_file = convert_to_binary_data(f"{username}.json")
    os.remove(f'{username}.json')
    add_event(username, json_binary_file)


def create_event_list():
    user_event = EventModel.query.filter_by(username=un.get_username()).first()
    json_binary_file = user_event.events
    write_to_file(json_binary_file, un.get_username())
    with open(f"{un.get_username()}.json", "r") as read_file:
        event_list = json.load(read_file)
    os.remove(f"{un.get_username()}.json")
    return event_list


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
