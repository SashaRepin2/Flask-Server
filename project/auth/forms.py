from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import Email, DataRequired, Length, EqualTo, AnyOf, InputRequired, ValidationError

from project.models import User


class RegistrationForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(message="Необходимо ввести Почту"),
                                               Email(message="Введеная почта является невалидной"),
                                               Length(max=50,
                                                      message="Длина почты не должна превышать 50 символов")])
    last_name = StringField("Last name: ",
                            validators=[DataRequired(message="Необходимо ввести Фамилию"),
                                        Length(max=25, message="Длина фамилии не должна превышать 25 символов")])
    first_name = StringField("First name: ",
                             validators=[DataRequired(message="Необходимо ввести Имя"),
                                         Length(max=25, message="Длина имени не должна превышать 25 символов")])
    login = StringField("Login: ", validators=[DataRequired(message="Необходимо ввести логин"),
                                               Length(max=25, message="Длина логина не должна превышать 25 символов")])
    password = PasswordField("Password: ",
                             validators=[DataRequired(message="Необходимо ввести пароль"),
                                         Length(min=4, max=50, message="Длина пароля должна быть от 4 до 50 символов"),
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
            raise ValidationError('Почта уже занята')


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[DataRequired(), Email(), Length(min=1, max=50)])
    password = PasswordField("Password: ", validators=[Length(max=50)])
    remember = BooleanField('Remember me')
    submit = SubmitField("Log in")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        # Check password
        if user is None or not user.verify_password(self.password.data):
            raise ValidationError('Неверная почта или пароль')
