from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Email, DataRequired, Length, EqualTo, AnyOf, InputRequired, ValidationError

from project.models import User


class RegistrationForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(message="Необходимо ввести Почту"),
                                               Email(message="Введеная почта является невалидной"),
                                               Length(min=1, max=50,
                                                      message="Длина почты не должна превышать 50 символов")])
    last_name = StringField("Last name: ",
                            validators=[DataRequired(message="Необходимо ввести Фамилию"), Length(min=4, max=50)])
    first_name = StringField("First name: ",
                             validators=[DataRequired(message="Необходимо ввести Имя"), Length(min=2, max=50)])
    login = StringField("Login: ", validators=[DataRequired(message="Необходимо ввести логин")])
    password = PasswordField("Password: ",
                             validators=[DataRequired(message="Необходимо ввести пароль"), Length(min=4, max=50),
                                         EqualTo('password_confirmation',
                                                 message='Пароли должны совпадать')])
    password_confirmation = PasswordField('Confirm password:')
    age = SelectField("Age: ", choices=[('adult', 'Older than 18'), ('child', 'Less than 18')],
                      validators=[AnyOf(values=['adult'], message="Возраст меньше 18 лет")])
    gender = SelectField("Gender: ", choices=[('male', 'Male'), ('female', 'Female')])
    agreement = BooleanField("Agreement",
                             validators=[InputRequired(message="Необходимо принять пользовательское соглашание")])
    submit = SubmitField("Register")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField("Password: ", validators=[Length(max=50)])
    remember = BooleanField('Remember me')
    submit = SubmitField("Log in")
