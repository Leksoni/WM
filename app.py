from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import exc

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisissecreykeywhichissecret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    facebook = db.Column(db.String(50))
    location = db.Column(db.String(50))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    username = StringField("username", validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField("password", validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField("remember")


class RegisterForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), Email(
        message="Invalid email"), Length(max=50)])
    username = StringField("username", validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField("password", validators=[
                             InputRequired(), Length(min=8, max=80)])
    facebook = StringField("facebook", validators=[
                           InputRequired(), Length(max=50)])
    location = StringField("location", validators=[
                           InputRequired(), Length(max=50)])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('dashboard'))

        return redirect(url_for('loginError'))

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(
            form.password.data, method='sha256')
        try:
            new_user = User(username=form.username.data, email=form.email.data,
                            location=form.location.data,  password=hashed_password,
                            facebook=form.facebook.data)
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            return redirect(url_for('registerError'))

        return redirect(url_for('login'))

    return render_template("register.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    users = User.query.filter().all()
    inputValue = request.args.get('loc')
    if(inputValue == None):
        inputValue = "searched location"
    userLocation = User.query.filter_by(location=inputValue).all()
    return render_template('dashboard.html', users=users, name=current_user.username, userLocation=userLocation, inputValue=inputValue)


@app.route("/loginError")
def loginError():
    return render_template("loginError.html")


@app.route("/registerError")
def registerError():
    return render_template("registerError.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


if (__name__) == "__main__":
    app.run(debug=True)
