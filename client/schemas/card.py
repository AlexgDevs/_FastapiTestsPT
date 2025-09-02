from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from flask_wtf import FlaskForm


class CreateCardForm(FlaskForm):
    cardholder_name = StringField('Название карты', validators=[
        DataRequired()
    ])

    submit = SubmitField('Привязать карту')