from flask import Flask, request, make_response, redirect, render_template, url_for, send_file
from data import db_session, tables
from flask_restful import reqparse, abort, Api, Resource

import forms
import stuff

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZxrC#@wx-%08xKA9w-#ug2YB8c-A4IWoN#y'
api = Api(app)

app.jinja_env.globals['data'] = stuff.get_table
app.jinja_env.globals['entry'] = stuff.get_entry


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


@app.route('/clients', methods=['POST', 'GET'])
def clients():
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    user = stuff.get_user(username)
    if not user.role in ('manager', 'all_in'):
        return redirect('/dashboard')
    if request.method == 'GET':
        return render_template('clients.html', sort='id',
                               reverse=0, role=user.role, title=f'{user.role} ({user.name})')
    elif request.method == 'POST':
        stuff.update_entry('clients', request.form)
        return redirect('/clients')


@app.route('/tables/<table>', methods=['POST', 'GET'])
def tables(table):
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    user = stuff.get_user(username)
    if user.role == 'manager' and not table in ('clients', 'orders') or\
        user.role == 'courier' and not table in ('orders', 'acceptances', 'things', 'shipments') or\
        user.role == 'worker' and not table in ('acceptances', 'works'):
        return redirect('/dashboard')
    if request.method == 'GET':
        return render_template(f'{table}.html', sort='id',
                               reverse=0, role=user.role, title=f'{user.role} ({user.name})')
    elif request.method == 'POST':
        stuff.update_entry(table, request.form)
        return redirect(f'/tables/{table}')


def main():
    db_session.global_init("db/data.db")
    app.run(port=8080, host='192.168.0.14')


if __name__ == '__main__':
    main()
