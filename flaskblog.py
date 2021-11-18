from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

# Secret key to protect against modifying cookies and cross-site forgery attacks
app.config['SECRET_KEY'] = "a40fbbb5e9691778bfcf707d3c559c2f"

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

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title="Register", form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title="Login", form=form)

# Use `python flaskblog.py` to run in debug
if __name__ == "__main__":
    app.run(debug=True)

# To run without debug you could set debug=False or
# set the environment variables `export FLASK_APP=flaskblog` and run `flask run`
