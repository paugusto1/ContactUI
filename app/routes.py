import ssl
from datetime import datetime

import flask
from flask import render_template, request
from flask_cors import cross_origin
from app import application, csrf

from flask import render_template, flash, redirect
from app import application
from app.forms import LoginForm, UpdateForm, SearchForm, CreateForm
import urllib.request, json
import requests

from modelsClasses import Contact, PersonDetails, EmailSingle, PhoneNumberSingle, AddressSingle, Email, PhoneNumber, \
    Address

#Production API URL
#URL = 'https://6ahjvquitxcghde3f4jihyjwcy0vqnov.lambda-url.us-east-1.on.aws'

#TEST API URL (Same DB)
URL = 'http://127.0.0.1:8000'

def getContactFromForm(form):

    personDetail = PersonDetails(firstName=form.firstName.data, lastName=form.lastName.data,
                                 dateOfBirth=form.dateOfBirth.data.strftime(format = '%Y-%m-%d'))

    emails = []

    if form.personalEmail.data != '':
        emailP = EmailSingle(type='PERSONAL', value=form.personalEmail.data)
        emails.append(emailP)
    if form.workEmail.data != '':
        emailW = EmailSingle(type='WORK', value=form.personalEmail.data)
        emails.append(emailW)

    emailL = Email(__root__=emails)

    phones = []

    if form.homePhone.data != '':
        phoneP = PhoneNumberSingle(type='PERSONAL', value=form.homePhone.data)
        phones.append(phoneP)
    if form.workPhone.data != '':
        phoneW = PhoneNumberSingle(type='WORK', value=form.workPhone.data)
        phones.append(phoneW)

    phoneL = PhoneNumber(__root__=phones)

    addresses = []

    if form.postalCode.data != '':
        add = AddressSingle(apartment=form.apartment.data, street=form.street.data + ',' + str(form.number.data),
                            city=form.city.data, state=form.state.data, postalCode=form.postalCode.data,
                            country=form.country.data)

        addresses.append(add)

    addL = Address(__root__=addresses)

    newContact = Contact(id=1, personDetails=personDetail, company=form.company.data,
                         profileImage=form.profileImage.data, email=emailL, phoneNumber=phoneL, address=addL)

    return newContact



@application.route('/')
@application.route('/index')
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


@application.route('/list', methods=['GET', 'POST'])
def listContacts():

    url = URL + "/get-contacts/all"

    response = urllib.request.urlopen(url)

    data = response.read()

    dict = json.loads(data)

    form = LoginForm()

    return render_template('list.html', title='All contacts', form=form, contacts=dict)

@application.route('/update/<contactId>', methods=['GET', 'POST'])
def updateContact(contactId):

    url = URL+ "/get-contacts/id/" + contactId

    response = urllib.request.urlopen(url)

    data = response.read()
    dict = json.loads(data)

    form = UpdateForm()

    if request.method == 'POST':
        t = request.form


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

        url = URL+ "/update-contact/" + str(contactId)

        newContact = getContactFromForm(form)
        newContact.id = contactId

        try:
            response = requests.put(url, newContact.json())
        except:
            return render_template('errorSSL.html', title='SSL error', contact=newContact.json(), url = url)

        if response.status_code == 200:
            form = LoginForm()

            return render_template('index.html', title='Contact Updated', form=form, updated=True)

        else:
            return render_template('update.html', title='Update Contact', form=form, contacts=dict, error=response.content)


    response = flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return render_template('update.html', title='Update Contact', form = form, contacts=dict)

@application.route('/add', methods=['GET', 'POST'])
def addContact():

    form = CreateForm()

    if form.validate_on_submit():

        url = URL+ "/create-contact/"

        newContact = getContactFromForm(form)

        try:
            response = requests.post(url, newContact.json())
        except:
            return render_template('errorSSL.html', title='SSL error', contact=newContact.json(), url = url)


        if response.status_code == 200:
            form = LoginForm()

            return render_template('index.html', title='Contact Added', form=form, added=True)

        else:
            return render_template('add.html', title='Add Contact', form=form, contacts=dict, error = response.content)

    response = flask.jsonify({'some': 'data'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return render_template('add.html', title='Update Contact', form = form)

@application.route('/search', methods=['GET', 'POST'])
def search():

    form = SearchForm()

    if form.validate_on_submit():
        url = URL+ "/get-contacts/%s/%s" % (form.field.data, form.value.data)

        response = urllib.request.urlopen(url)

        data = response.read()

        dict = json.loads(data)

        form = LoginForm()

        return render_template('list.html', title='Search results', form=form, contacts=dict, search = True)

    return render_template('search.html', title='Search contacts', form=form)

@application.route('/delete/<contactId>', methods=['GET', 'POST'])
def deleteContact(contactId):

    url = URL+ "/delete-contact/" + contactId

    response = requests.delete(url)


    if response.status_code == 200:
        deleted = True
    else:
        deleted = False

    url = URL+ "/get-contacts/all"

    response = urllib.request.urlopen(url)

    data = response.read()

    dict = json.loads(data)

    form = LoginForm()

    return render_template('list.html', title='All contacts', form=form, contacts=dict, deleted = deleted)

#For test only
@application.route('/reset', methods=['GET', 'POST'])
def resetDB():

    url = URL + "/populate-db/test-only"

    response = urllib.request.urlopen(url)

    data = response.read()

    return render_template('index.html', title='Database reset', reset=True)





