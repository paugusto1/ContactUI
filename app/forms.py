from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, URL, Optional, Email, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateForm(FlaskForm):

    firstName = StringField('First Name', validators=[DataRequired()], render_kw={'readonly':''})
    lastName = StringField('Last Name', validators=[DataRequired()], render_kw={'readonly':''})
    dateOfBirth = DateField('Birthday', validators=[Optional()])
    profileImage = StringField('Profile Image URL', validators=[Optional(), URL()])

    homePhone = StringField('Home Phone Number', validators=[Optional()],
                            render_kw={'pattern' : "^(\\([0-9]{2}\\))?[0-9]{4,5}-?[0-9]{4}$"})
    workPhone = StringField('Work Phone Number', validators=[Optional()],
                            render_kw={'pattern' : "^(\\([0-9]{2}\\))?[0-9]{4,5}-?[0-9]{4}$"})
    personalEmail = StringField('Personal Email', validators=[Email(), Optional()])
    workEmail = StringField('Work Email', validators=[Email(), Optional()])

    company = StringField('Company', validators=[Optional()])

    apartment = StringField('Apartament', validators=[Optional()])
    street = StringField('Street', validators=[Optional()], render_kw={'readonly':''})
    number = IntegerField('Number', validators=[Optional(), NumberRange(min=0)])
    city = StringField('City', validators=[Optional()], render_kw={'readonly':''})
    state = StringField('State', validators=[Optional()], render_kw={'readonly':''})
    postalCode = StringField('Postal Code', validators=[DataRequired()], render_kw={'pattern' : '\d{5}-?\d{3}'})
    country = StringField('Country', validators=[Optional()], render_kw={'readonly':''})

    submit = SubmitField('Save')

class CreateForm(FlaskForm):

    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    dateOfBirth = DateField('Birthday', validators=[Optional()])
    profileImage = StringField('Profile Image URL', validators=[Optional(), URL()])

    homePhone = StringField('Home Phone Number', validators=[Optional()],
                            render_kw={'pattern' : "^(\\([0-9]{2}\\))?[0-9]{4,5}-?[0-9]{4}$"})
    workPhone = StringField('Work Phone Number', validators=[Optional()],
                            render_kw={'pattern' : "^(\\([0-9]{2}\\))?[0-9]{4,5}-?[0-9]{4}$"})
    personalEmail = StringField('Personal Email', validators=[Email(), Optional()])
    workEmail = StringField('Work Email', validators=[Email(), Optional()])

    company = StringField('Company', validators=[Optional()])

    apartment = StringField('Apartament', validators=[Optional()])
    street = StringField('Street', validators=[Optional()], render_kw={'readonly':''})
    number = IntegerField('Number', validators=[Optional(), NumberRange(min=0)])
    city = StringField('City', validators=[Optional()], render_kw={'readonly':''})
    state = StringField('State', validators=[Optional()], render_kw={'readonly':''})
    postalCode = StringField('Postal Code', validators=[DataRequired()], render_kw={'pattern' : '\d{5}-?\d{3}'})
    country = StringField('Country', validators=[Optional()], render_kw={'readonly':''})

    submit = SubmitField('Create')

class SearchForm(FlaskForm):

    value = StringField('Value', validators=[DataRequired()])
    field = SelectField('Field', choices=[('phone', 'Phone Number'), ('email', 'Email'),
                                          ('city', 'City'), ('state', 'State')])

    submit = SubmitField('Search')

