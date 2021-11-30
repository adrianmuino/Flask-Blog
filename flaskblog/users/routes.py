from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, AccountUpdateForm,
                                   RequestResetForm, ResetForm)
from flaskblog.users.utils import save_profile_pic, send_reset_email
from flaskblog.utils import est_read_time

users = Blueprint('users', __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=form.remember_me.data)
        flash("Account for {} successfully created.".format(form.username.data), category="success")
        return redirect(url_for("main.home"))
    return render_template("register.html", title="Register", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Invalid username and password!".format(form.username.data), category="danger")
    return render_template("login.html", title="Login", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("users.login"))

@users.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form)

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blogs = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=2, page=page)
    pages = blogs.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2)
    return render_template("user.html", user=user, blogs=blogs, pages=pages, est_read_time=est_read_time)

@users.route("/request_reset", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Email sent to {}.".format(user.email), category="info")
    return render_template("request_reset.html", title="Request Password Reset", form=form)

@users.route("/reset_password/<string:token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid or expired reset token", category="warning")
        redirect(url_for("users.request_reset"))
    form = ResetForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_pwd
        db.session.commit()
        flash("Password successfully updated.", category="success")
        return redirect(url_for("users.login"))
    return render_template("reset_password.html", title="Password Reset", form=form)