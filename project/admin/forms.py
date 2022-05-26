from flask import current_app
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, ValidationError, InputRequired


class GetAdminRole(FlaskForm):
    code = StringField('Секретный код', validators=[DataRequired('Необходимо ввести секретный код')])
    submit = SubmitField()

    def validate_code(self, field):
        if field.data != current_app.config['SECRET_KEY']:
            raise ValidationError('Неверный код')


class AcceptedBlogForm(FlaskForm):
    class Meta:
        csrf = False

    accepted = BooleanField('Одобрить')
    submit = SubmitField()
