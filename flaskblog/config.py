import json

with open('/etc/config.json') as config_file:
    config = json.load(config_file)

class Config:
    # Secret key to protect against modifying cookies and cross-site forgery attacks
    SECRET_KEY = config["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = config["SQLALCHEMY_DATABASE_URI"]
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = config["MAIL_USERNAME"]
    MAIL_DEFAULT_SENDER = ("Flask Blog", MAIL_USERNAME)
    MAIL_PASSWORD = config["MAIL_PASSWORD"]