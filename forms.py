from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, StopValidation

import stuff


class CorrectData:
    def __call__(self, form, field):
        user = stuff.check_user(field.data)
        if user:
            if form.data['password'] == user[0][1]:
                return
            raise StopValidation('password incorrect')
        raise StopValidation('user does not exist')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), CorrectData()])
    password = PasswordField('Пароль')
    submit = SubmitField('Войти')
