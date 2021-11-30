from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
import flaskblog.utils as utils

class PostForm(FlaskForm):
    title = StringField("Title",
                           validators=[DataRequired(), Length(max=utils.POST_TITLE_LEN)])
    content = TextAreaField("Content", validators=[DataRequired()])
    create = SubmitField("Create")