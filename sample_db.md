Run these commands in a bash shell to create a sample DB.

Here we also modify and read/write to the sample DB.

## NOTE:
To follow this tutorial you need to have installed the dependencies in `requirements.txt`.

You can run `./dependencies/pip_dep_install.sh` to install these. _It is recommended to run the previous command inside your python virtual environment._

### Start python interpreter shell
```bash
python
```

### Create DB
```python
from flaskblog import db
db.create_all()
```

### Add two users to the DB
```python
from flaskblog.models import User, Post
user_1 = User(username="adrianmuino", email="a@email.com", password="password123")
db.session.add(user_1)
user_2 = User(username="joesmith10", email="joe@sample.com", password="wordpass321")
db.session.add(user_2)
db.session.commit()
```

### Sample DB User queries
```python
User.query.all()
User.query.first()
User.query.filter_by(username="adrianmuino").all()
User.query.filter_by(username="adrianmuino").first()
user = User.query.filter_by(username="joesmith10").first()
user
user.id
user = user.query.get(1)
user
user.posts
```

### Add posts to the DB
```python
user.id
post_1 = Post(title="Blog 1", content="This is a sample content for the first blog", user_id=user.id)
post_2 = Post(title="Blog 2", content="Second blog content. Cool!", user_id=user.id)
user = User.query.filter_by(username="joesmith10").first()
post_3 = Post(title="Blog 3", content="This blog posting app is getting interesting <3", user_id=user.id)
db.session.add(post_1)
db.session.add(post_2)
db.session.add(post_3)
db.session.commit()
```

### Sample DB Post queries
```python
user.posts
for post in user.posts:
    print(post.title)

posts = Post.query.all()  # EXPENSIVE!!! Consider pagination.
for post in posts:
    print("{} by {}".format(post.title, post.author.username))
    print("{}\n".format(post.content))

post = Post.query.first()
post
post.user_id
post.author
```

### Post pagination
``` python
posts = Post.query.paginate(per_page=5)
posts.page  # Get current page number
for post in posts.items:
    print(post.title)

posts = Post.query.paginate(per_page=2, page=3)    # Get page 3 with 2 posts per page
for page in posts.iter_pages(left_edge=1, right_edge=1, left_current=1, right_current=2):
    print(page)

posts.total  # Get total number of posts
```

### Drop all database tables (user and post tables)
```python
db.drop_all()
exit()
```