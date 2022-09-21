from flask import render_template
from app import app

from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
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
    return render_template('list.html', title='Sign In', form=form, info=table)