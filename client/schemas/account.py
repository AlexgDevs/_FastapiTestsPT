from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flask_wtf import FlaskForm


class CreateAccountForm(FlaskForm):
    account_name = StringField('Название счета', validators=[
        Length(min=3, max=150),
        DataRequired()
    ])

    submit = SubmitField('Создать счет')