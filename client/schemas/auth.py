from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flask_wtf import FlaskForm
from passlib.context import CryptContext

from ..db import Session, User, select
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegistrationForm(FlaskForm):
    name = StringField('Имя пользователя',
                    validators=[
                    DataRequired(message='Обязательное поле'),
                    Length(
                    min=3, max=20, message='Имя должно быть от 3 до 20 символов')
                    ])

    email = StringField('Email',
                        validators=[
                        DataRequired(message='Обязательное поле'),
                        ])

    password = PasswordField('Пароль',
                        validators=[
                        DataRequired(message='Обязательное поле'),
                        Length(min=6, message='Пароль должен быть не менее 6 символов')
                        ])

    confirm_password = PasswordField('Подтверждение пароля',
                            validators=[
                            DataRequired(message='Обязательное поле'),
                            EqualTo('password', message='Пароли не совпадают')
                            ])

    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    name = StringField('Имя пользователя',
                    validators=[DataRequired(message='Обязательное поле')
                    ])

    password = PasswordField('Пароль',
                        validators=[DataRequired(message='Обязательное поле')
                        ])


    async def validate_password(self, field):
        async with Session() as session:
            user = await session.scalar(
                select(User)
                .where(User.name == self.name.data)
                )

            if user:
                if not pwd_context.verify(field.data, user.password):
                    raise ValidationError('Неверный пароль')
            else:
                raise ValidationError('Неверный логин или пароль')

    submit = SubmitField('Войти')
