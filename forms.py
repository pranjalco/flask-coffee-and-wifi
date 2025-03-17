from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField(label='Cafe Location in Google Maps (URL)', validators=[DataRequired(), URL(require_tld=True)])
    open_time = StringField(label='Opening Time e.g.9AM', validators=[DataRequired()])
    close_time = StringField(label='Closing Time e.g. 7PM', validators=[DataRequired()])
    coffee_rating = SelectField(label='Coffee Rating', choices=[('☕️️️', '☕️'), ('☕️☕️️️', '☕️☕️️️'), ('☕️☕️☕️️️', '☕️☕️☕️️️️️'), ('☕️☕️☕️☕️️️', '☕️☕️☕️☕️️️'), ('☕️☕️☕️☕️☕️️️', '☕️☕️☕️☕️☕️️️')])
    wifi_rating = SelectField(label="Wifi Strength Rating", choices=[('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪'), ('💪💪💪💪💪', '💪💪💪💪💪')])
    power_choices = [('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')]
    power_socket = SelectField(label="Power Socket Availability", choices=power_choices)

    submit = SubmitField(label='Submit')


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField("LOGIN")


class RegisterForm(FlaskForm):
    name = StringField(label="Name", validators=[DataRequired()])
    email = StringField(label="Email", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])

    submit = SubmitField(label="REGISTER")
