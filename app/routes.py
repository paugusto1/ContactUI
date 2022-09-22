from datetime import datetime

import flask
from flask import render_template, request
from flask_cors import cross_origin

from app import app

from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, UpdateForm
import urllib.request, json
#from app.table import table
import pandas as pd

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/contact/<contactname>')
def user(contactname):
    user = contactname
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('contact.html', user=user, posts=posts)

@app.route('/list', methods=['GET', 'POST'])
def listContacts():

    url = "http://127.0.0.1:8000/get-contacts/all"

    response = urllib.request.urlopen(url)


    data = response.read()
    print(data)
    print(type(data))
    dict = json.loads(data)
    print(dict[0]['personDetails'])
    print(type(dict))

    df = pd.DataFrame(dict)
    table = df.to_html(index=False)

    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('list.html', title='All contacts', form=form, contacts=dict)

@app.route('/update/<contactId>', methods=['GET', 'POST'])
def updateContact(contactId):

    url = "http://127.0.0.1:8000/get-contacts/id/" + contactId

    response = urllib.request.urlopen(url)

    data = response.read()
    dict = json.loads(data)

    form = UpdateForm()

    print(form.errors)

    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)

    if request.method == 'POST':
        t = request.form
        print(t)


    date = datetime.strptime(dict[0]['personDetails']['dateOfBirth'], '%Y-%m-%d')

    if len(dict[0]['email']) == 1:
        personalEmail = dict[0]['email'][0]['value']
        workEmail = ''
    elif len(dict[0]['email']) == 2:
        personalEmail = dict[0]['email'][0]['value']
        workEmail = dict[0]['email'][1]['value']
    elif len(dict[0]['email']) == 0:
        personalEmail = ''
        workEmail = ''

    if len(dict[0]['phoneNumber']) == 1:
        personalPhone = dict[0]['phoneNumber'][0]['value']
        workPhone = ''
    elif len(dict[0]['phoneNumber']) == 2:
        personalPhone = dict[0]['phoneNumber'][0]['value']
        workPhone = dict[0]['phoneNumber'][1]['value']
    elif len(dict[0]['phoneNumber']) == 0:
        personalPhone = ''
        workPhone = ''

    if len(dict[0]['address']) > 0:
        apartment = dict[0]['address'][0]['apartment']
        street = dict[0]['address'][0]['street'].split(',')[0]
        number = dict[0]['address'][0]['street'].split(',')[1]
        city = dict[0]['address'][0]['city']
        state = dict[0]['address'][0]['state']
        postalCode = dict[0]['address'][0]['postalCode']
        country = dict[0]['address'][0]['country']
    else:
        apartment = ''
        street = ''
        city = ''
        state = ''
        postalCode = ''
        country = ''


    form = UpdateForm(firstName = dict[0]['personDetails']['firstName'],
                      lastName = dict[0]['personDetails']['lastName'],
                      dateOfBirth = date,
                      profileImage = dict[0]['profileImage'],
                      company = dict[0]['company'],
                      homePhone=personalPhone,
                      workPhone=workPhone,
                      personalEmail=personalEmail,
                      workEmail=workEmail,
                      apartment=apartment,
                      street = street,
                      city = city,
                      state = state,
                      postalCode = postalCode,
                      country = country,
                      number = number
                      )

    if form.validate_on_submit():
        return redirect('/index')

    response = flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return render_template('update.html', title='Update Contact', form = form, contacts=dict)

@app.route('/add', methods=['GET', 'POST'])
def addContact():

    form = UpdateForm()

    print(form.errors)

    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)


    form = UpdateForm()

    if form.validate_on_submit():
        return redirect('/index')

    response = flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return render_template('add.html', title='Update Contact', form = form)
