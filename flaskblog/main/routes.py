from flask import render_template, request, Blueprint
from flask_login import login_required
from flaskblog.models import Post
from flaskblog.utils import est_read_time

main = Blueprint('main', __name__)

@main.route("/home")
@main.route("/")
@login_required
def home():
    page = request.args.get("page", type=int)    # Get page param, if there's no page param then default is 1. If param value is not an int then throw 404 error
    blogs = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    pages = blogs.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2)
    return render_template("index.html", blogs=blogs, pages=pages, est_read_time=est_read_time)

@main.route("/about")
def about():
    return render_template("about.html", title="About")