from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Secret key to protect against modifying cookies and cross-site forgery attacks
app.config['SECRET_KEY'] = "a40fbbb5e9691778bfcf707d3c559c2f"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)

import flaskblog.routes as routes