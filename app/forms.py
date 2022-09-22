from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, URL, Optional, Email, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateForm(FlaskForm):

    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    dateOfBirth = DateField('Birthday', validators=[Optional()])
    profileImage = StringField('Profile Image URL', validators=[Optional(), URL()])

    homePhone = StringField('Home Phone Number', validators=[Optional()], render_kw={'pattern' : '^\s*(\d{2}|\d{0})[-. ]?(\d{5}|\d{4})[-. ]?(\d{4})[-. ]?\s*$'})
    workPhone = StringField('Work Phone Number', validators=[Optional()], render_kw={'pattern' : '^\s*(\d{2}|\d{0})[-. ]?(\d{5}|\d{4})[-. ]?(\d{4})[-. ]?\s*$'})
    personalEmail = StringField('Personal Email', validators=[Email()])
    workEmail = StringField('Work Email', validators=[Email()])

    company = StringField('Company', validators=[Optional()])

    apartment = StringField('Apartament', validators=[Optional()])
    street = StringField('Street', validators=[Optional()], render_kw={'disabled':''})
    number = IntegerField('Number', validators=[DataRequired(), NumberRange(min=0)])
    city = StringField('City', validators=[Optional()], render_kw={'disabled':''})
    state = StringField('State', validators=[Optional()], render_kw={'disabled':''})
    postalCode = StringField('Postal Code', validators=[DataRequired()], render_kw={'pattern' : '\d{5}-?\d{3}'})
    country = StringField('Country', validators=[Optional()], render_kw={'disabled':''})

    submit = SubmitField('Save')

