from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired


class PostForm(FlaskForm):
    title = StringField("Title: ", validators=[DataRequired(), Length(min=1, max=100,
                                                                      message="Заголовок должен быть больше 100 символов")])
    body = StringField("Body: ", validators=[DataRequired(), Length(min=1, max=500,
                                                                    message="Содержание статьи должно превышать 500 символов")])
    submit = SubmitField("Create")
