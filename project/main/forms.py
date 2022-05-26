from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import Length, DataRequired


class BlogForm(FlaskForm):
    title = StringField("Title: ", validators=[DataRequired(), Length(max=25,

                                                                      message="Заголовок не должен быть больше 25 символов")])
    description = StringField("Description", validators=[DataRequired(), Length(max=50,
                                                                                message="Описание не должно превышать длины в 50 символов")])

    preview_image = FileField("Preview")
    content = TextAreaField("Content: ", validators=[DataRequired()])
    submit = SubmitField("Create")


class CommentForm(FlaskForm):
    body = StringField('Введите ваш комментарий', validators=[DataRequired()])
    submit = SubmitField('Submit')
