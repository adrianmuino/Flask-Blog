import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

# This func can be improved to query db and make sure the generated unique hex_str is unique, else images with same name are overwritten
def save_profile_pic(form_img_file):
    hex_str = secrets.token_hex(16)
    _, f_ext = os.path.splitext(form_img_file.filename)
    hex_img_file = "{}{}".format(hex_str, f_ext)
    img_path = os.path.join(current_app.root_path, "static/profile_pics", hex_img_file)
    # Save image resized to size used in `main.css` to save space in our filesystem
    size = (125, 125)
    img = Image.open(form_img_file)
    img.thumbnail(size)
    img.save(img_path)
    return hex_img_file

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Request for Password Reset",
                  recipients = [user.email])
    msg.body = """Visit the following link to reset your password: {}

If you did not request a password reset you can ignore this email.
    """.format(url_for('users.reset_password', token=token, _external=True)) # We need absolute url, not relative url
    mail.send(msg)