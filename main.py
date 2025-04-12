from flask import Flask, request, make_response, redirect, render_template, url_for, send_file
from data import db_session, tables
from flask_restful import reqparse, abort, Api, Resource

import forms
import stuff

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZxrC#@wx-%08xKA9w-#ug2YB8c-A4IWoN#y'
api = Api(app)


@app.route('/')
def index():
    user = request.cookies.get('user')
    if user:
        return redirect('/dashboard')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        global username
        global user
        resp = redirect('/dashboard')
        resp.set_cookie('user', form.data['username'])
        return resp
    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    user = stuff.get_user(username)
    return render_template('dashboard.html',
                           role=user.role, title=f'{user.role} ({user.name})')
    # return send_file(stuff.create_qr('http://192.168.0.4:8080/dashboard'), mimetype='image/png')


@app.route('/tables/<table>')
def tables(table):
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    user = stuff.get_user(username)
    if user.role == 'manager' and not table in ('clients', 'orders') or\
        user.role == 'courier' and not table in ('orders', 'acceptances', 'things', 'shipments') or\
        user.role == 'worker' and not table in ('acceptances', 'works'):
        return redirect('/dashboard')
    return render_template('table.html',
                           table=table, role=user.role, title=f'{user.role} ({user.name})')


def main():
    db_session.global_init("db/data.db")
    app.run(port=8080, host='127.0.0.1')


if __name__ == '__main__':
    main()
