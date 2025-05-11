from json import loads, dumps

from flask import Flask, request, make_response, redirect, render_template, send_file, jsonify
from data import db_session
from data import crm_api
from data.tables import *
from flask_restful import reqparse, abort, Api, Resource

import forms
import stuff

from socket import gethostbyname, gethostname
LOCAL_IP = gethostbyname(gethostname())

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ZxrC#@wx-%08xKA9w-#ug2YB8c-A4IWoN#y'
api = Api(app)

app.jinja_env.globals['data'] = stuff.get_table
'''app.jinja_env.globals['entry'] = stuff.get_entry'''


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
    return render_template('dashboard.html', user=user)


@app.route('/tables/<table>', methods=['POST', 'GET'])
def tables(table):
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    user = stuff.get_user(username)
    if user.role == 'manager' and not table in ('clients', 'orders', 'acceptances', 'things') or \
            user.role == 'courier' and not table in ('orders', 'acceptances', 'things', 'shipments') or \
            user.role == 'worker' and not table in ('acceptances', 'works'):
        return redirect('/dashboard')
    if request.method == 'GET':
        return render_template(f'{table}.html', sort='id', reverse=0, user=user)
    elif request.method == 'POST':
        stuff.update_entry(table, request.form)
        return redirect(f'/tables/{table}')


@app.route('/tables/acceptances/<int:acceptance_id>', methods=['GET', 'POST'])
def acceptance(acceptance_id):
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    user = stuff.get_user(username)
    if request.method == 'GET':
        data = stuff.get_entry('acceptances', acceptance_id)
        things = stuff.get_table('things').filter(Thing.id.in_(loads(data.things)))
        resp = make_response(render_template('acceptance.html', user=user,
                                             acceptance=data, things=things))
        resp.set_cookie('acceptance', str(acceptance_id))
        return resp
    elif request.method == 'POST':
        stuff.update_entry('acceptances', request.form)
        return redirect(f'/tables/acceptances/{acceptance_id}')


@app.route('/tables/acceptances/<int:acceptance_id>/remove_thing/<int:thing_id>')
def remove_thing(acceptance_id, thing_id):
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    stuff.remove_thing_from_acceptance(acceptance_id, thing_id)
    return redirect(f'/tables/acceptances/{acceptance_id}')


@app.route('/tables/acceptances/<acceptance_id>/add_thing/<int:thing_id>')
def add_thing(acceptance_id, thing_id):
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    stuff.add_thing_to_acceptance(acceptance_id, thing_id)
    return redirect(f'/tables/acceptances/{acceptance_id}')


@app.route('/tables/things/<int:thing_id>', methods=['GET', 'POST'])
def thing(thing_id):
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    user = stuff.get_user(username)
    if request.method == 'GET':
        return render_template(f'thing.html', user=user,
                               acceptance=stuff.get_entry('acceptances', int(request.cookies.get('acceptance'))),
                               thing=stuff.get_entry('things', thing_id),
                               works=stuff.get_table('works').filter(Work.thing_id == thing_id))
    elif request.method == 'POST':
        stuff.update_entry('things', request.form)
        return redirect(f'/tables/thing/{thing_id}')


@app.route('/tables/things/<int:thing_id>/qr')
def thing_qr(thing_id):
    return send_file(stuff.create_qr(f'http://{LOCAL_IP}:8080/tables/things/{thing_id}'), mimetype='image/png')


@app.route('/tables/works/<int:work_id>', methods=['GET', 'POST'])
def work(work_id):
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    user = stuff.get_user(username)
    if request.method == 'GET':
        return render_template(f'work.html', user=user, work=stuff.get_entry('works', work_id))
    elif request.method == 'POST':
        stuff.update_entry('works', request.form)
        return redirect(f'/tables/works/{work_id}')


@app.route('/tables/works/new/<int:thing_id>')
def new_work(thing_id):
    username = request.cookies.get('user')
    if not username:
        return redirect('/login')
    user = stuff.get_user(username)
    created_work = stuff.create_work(thing_id, user)
    if created_work:
        return redirect(f'/tables/works/{created_work.id}')
    else:
        return redirect(f'/tables/things/{thing_id}')


@app.route('/error')
def error():
    return render_template('error.html')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def main():
    print(LOCAL_IP)
    db_session.global_init("db/data.db")
    app.register_blueprint(crm_api.blueprint)
    app.run(port=8080, host=LOCAL_IP)


if __name__ == '__main__':
    main()
