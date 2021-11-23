from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, AccountUpdateForm
from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
import os, secrets
from PIL import Image

blogs = [
    {
        'author': "Adrian A. Muino",
        'title': "Writing My First Web App",
        'content': "This is a sample blog post about my first ever web application. Pretty cool!",
        'date_published': "Nov 16 2021"
    },
    {
        'author': "Jose Blake",
        'title': "Sample Post Title 2",
        'content': """This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.
                    This is another blog post just filling up some space.""",
        'date_published': "Oct 10 2021"
    },
    {
        'author': "Jane Blake",
        'title': "First Post",
        'content': "This is the first blog ever in the Flask site.",
        'date_published': "Jan 1 2000"
    }
]

# Adults average words per minute (reading)
avg_wpm = 200

for blog in blogs:
    blog['est_read_time'] = int(len(blog['content'].split())/avg_wpm)

@app.route("/")
@app.route("/home")
@login_required
def home():
    return render_template("index.html", blogs=blogs)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember_me.data)
        flash("Account for {} successfully created.".format(form.username.data), category="success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Invalid username and password!", category="danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# This func can be improved to query db and make sure the generated unique hex_str is unique, else images with same name are overwritten
def save_profile_pic(form_img_file):
    hex_str = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_img_file.filename)
    hex_img_file = "{}{}".format(hex_str, f_ext)
    img_path = os.path.join(app.root_path, "static/profile_pics", hex_img_file)
    # Save image resized to size used in `main.css` to save space in our filesystem
    size = (125, 125)
    img = Image.open(form_img_file)
    img.thumbnail(size)
    img.save(img_path)
    return hex_img_file

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:   # AccountUpdateForm() picture is not required in forms.py
            current_user.profile_img_file = save_profile_pic(form.picture.data) # Could be improved to also delete old profile_img from machine
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Account successfully update.", category="success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form)