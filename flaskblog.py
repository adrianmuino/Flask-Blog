from flask import Flask, render_template, url_for, flash, redirect
import forms
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Secret key to protect against modifying cookies and cross-site forgery attacks
app.config['SECRET_KEY'] = "a40fbbb5e9691778bfcf707d3c559c2f"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)

POST_TITLE_LEN = 100

# Each class inheriting from db.Model is a DB table
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(forms.USR_MAX_LEN), unique=True, nullable=False)
    email = db.Column(db.String(forms.EMAIL_MAX_LEN), unique=True, nullable=False)
    password = db.Column(db.String(forms.PASSWD_HASH_LEN), nullable=False)
    profile_img_file = db.Column(db.String(forms.FILENAME_LEN), nullable=False, default="default.jpg")
    # Additional query that gets all the user's posts lazily loaded (as they are needed)
    posts = db.relationship("Post", backref="author", lazy=True) # post.author is linked to User() class
    # Note: we can do `post.author` but know that this runs a query in the background b/c `author` is not an attribute in the post table

    def __repr__(self):
        return "User({}, {}, {})".format(self.username, self.email, self.profile_img_file)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(POST_TITLE_LEN), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # utcnow() func is the param
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) # primary key in the 'user' table

    def __repr__(self):
        return "Post({}, {})".format(self.title, self.date_posted)

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
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash("Account for {} successfully created.".format(form.username.data), category="success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        if form.username.data == "adrianmuino" and form.password.data == "asdfghjkl":
            return redirect(url_for("home"))
        else:
            flash("Invalid username and password!", category="danger")
    return render_template("login.html", title="Login", form=form)

# Use `python flaskblog.py` to run in debug
if __name__ == "__main__":
    app.run(debug=True)

# To run without debug you could set debug=False or
# set the environment variables `export FLASK_APP=flaskblog` and run `flask run`
