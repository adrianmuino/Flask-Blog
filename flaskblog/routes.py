from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect

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
def home():
    return render_template("index.html", blogs=blogs)

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Account for {} successfully created.".format(form.username.data), category="success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == "adrianmuino" and form.password.data == "asdfghjkl":
            return redirect(url_for("home"))
        else:
            flash("Invalid username and password!", category="danger")
    return render_template("login.html", title="Login", form=form)