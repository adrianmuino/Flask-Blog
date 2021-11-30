from flaskblog import db, login_manager
from flask import current_app
import flaskblog.utils as utils
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Each class inheriting from db.Model is a DB table
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(utils.USR_MAX_LEN), unique=True, nullable=False)
    email = db.Column(db.String(utils.EMAIL_MAX_LEN), unique=True, nullable=False)
    password = db.Column(db.String(utils.PASSWD_HASH_LEN), nullable=False)
    profile_img_file = db.Column(db.String(utils.FILENAME_LEN), nullable=False, default="default.jpg")
    # Additional query that gets all the user's posts lazily loaded (as they are needed)
    posts = db.relationship("Post", backref="author", lazy=True) # post.author is linked to User() class
    # Note: we can do `post.author` but know that this runs a query in the background b/c `author` is not an attribute in the post table

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id':self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return "User({}, {}, {})".format(self.username, self.email, self.profile_img_file)

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(utils.POST_TITLE_LEN), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # utcnow() func is the param
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False) # primary key in the 'user' table

    def __repr__(self):
        return "Post({}, {})".format(self.title, self.date_posted)