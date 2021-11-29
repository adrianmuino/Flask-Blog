from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, AccountUpdateForm,
                              PostForm, RequestResetForm, ResetForm)
from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
import os, secrets
from PIL import Image
from flask_mail import Message

# Adults average words per minute (reading)
avg_wpm = 200

@app.template_global()
def est_read_time(content):
    return int(len(content.split())/avg_wpm)

@app.route("/home")
@app.route("/")
@login_required
def home():
    page = request.args.get("page", type=int)    # Get page param, if there's no page param then default is 1. If param value is not an int then throw 404 error
    blogs = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    pages = blogs.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2)
    return render_template("index.html", blogs=blogs, pages=pages)

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
        if user:
            try:
                bcrypt.check_password_hash(user.password, form.password.data)
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for("home"))
            except:
                flash("Invalid username and password!", category="danger")
        else:
            flash("User {} does not exist!".format(form.username.data), category="danger")
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

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blogs = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=2, page=page)
    pages = blogs.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2)
    return render_template("user.html", user=user, blogs=blogs, pages=pages)

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Request for Password Reset",
                  sender = ("Flask Blog", app.config['MAIL_USERNAME']),
                  recipients = [user.email])
    msg.body = """Visit the following link to reset your password: {}

If you did not request a password reset you can ignore this email.
    """.format(url_for('reset_password', token=token, _external=True)) # We need absolute url, not relative url
    mail.send(msg)

@app.route("/request_reset", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Email sent to {}.".format(user.email), category="info")
    return render_template("request_reset.html", title="Request Password Reset", form=form)

@app.route("/reset_password/<string:token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Invalid or expired reset token", category="warning")
        redirect(url_for("request_reset"))
    form = ResetForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_pwd
        db.session.commit()
        flash("Password successfully updated.", category="success")
        return redirect(url_for("login"))
    return render_template("reset_password.html", title="Password Reset", form=form)

@app.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post was successfully created.", category="success")
        return redirect(url_for("home"))
    return render_template("create_post.html", form=form)

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", post=post)

@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post successfully updated.", category="success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form)

@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")
        return redirect(url_for("home"))