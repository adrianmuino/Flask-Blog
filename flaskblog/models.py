from flaskblog import db
import flaskblog.vars as vars
from datetime import datetime

# Each class inheriting from db.Model is a DB table
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(vars.USR_MAX_LEN), unique=True, nullable=False)
    email = db.Column(db.String(vars.EMAIL_MAX_LEN), unique=True, nullable=False)
    password = db.Column(db.String(vars.PASSWD_HASH_LEN), nullable=False)
    profile_img_file = db.Column(db.String(vars.FILENAME_LEN), nullable=False, default="default.jpg")
    # Additional query that gets all the user's posts lazily loaded (as they are needed)
    posts = db.relationship("Post", backref="author", lazy=True) # post.author is linked to User() class
    # Note: we can do `post.author` but know that this runs a query in the background b/c `author` is not an attribute in the post table

    def __repr__(self):
        return "User({}, {}, {})".format(self.username, self.email, self.profile_img_file)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(vars.POST_TITLE_LEN), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # utcnow() func is the param
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) # primary key in the 'user' table

    def __repr__(self):
        return "Post({}, {})".format(self.title, self.date_posted)