from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, StopValidation

from werkzeug.security import generate_password_hash, check_password_hash

import stuff


class CorrectData:
    def __call__(self, form, field):
        user = stuff.get_user(field.data)
        if user:
            if check_password_hash(user.password, form.data['password']):
                return
            raise StopValidation('password incorrect')
        raise StopValidation('user does not exist')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), CorrectData()])
    password = PasswordField('Пароль')
    submit = SubmitField('Войти')


class tableRowForm(FlaskForm):
    pass
