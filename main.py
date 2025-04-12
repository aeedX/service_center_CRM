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
        resp = redirect('/dashboard')
        resp.set_cookie('user', form.data['username'])
        return resp
    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    db_sess = db_session.create_session()
    username = request.cookies.get('user')
    user = db_sess.query(tables.Worker).filter(tables.Worker.username == username).first()
    title = f'{user.role} ({user.name})'
    return render_template(f'{user.role}-dashboard.html', title=title)
    # return send_file(stuff.create_qr('http://192.168.0.4:8080/dashboard'), mimetype='image/png')


def main():
    db_session.global_init("db/data.db")
    app.run(port=8080, host='192.168.0.4')


if __name__ == '__main__':
    main()
