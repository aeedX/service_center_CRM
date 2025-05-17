from json import loads

from flask import Flask, request, make_response, redirect, render_template, send_file, jsonify, current_app
from data import db_session
from data import restful_resources
import data
from data.tables import *
from flask_restful import Api
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from requests import get, post

import forms
import stuff

from socket import gethostbyname, gethostname

LOCAL_IP = gethostbyname(gethostname())

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'ZxrC#@wx-%08xKA9w-#ug2YB8c-A4IWoN#y'
api = Api(app)

app.jinja_env.globals['get_table'] = stuff.get_table
app.jinja_env.globals['Tables'] = data.tables
'''app.jinja_env.globals['entry'] = stuff.get_entry'''


@login_manager.user_loader
def load_user(worker_id):
    worker = stuff.db_sess.get(Worker, worker_id)
    return worker


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        db_sess = stuff.db_sess
        worker = db_sess.query(Worker).filter(Worker.username == form.username.data).first()
        if worker and worker.check_password(form.password.data):
            login_user(worker, remember=True)
            return redirect(request.cookies.get('redirect_target', '/dashboard'))
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/')
@app.route('/dashboard')
@stuff.login_and_role_required(current_user, '/dashboard')
def dashboard():
    return render_template('base.html', user=current_user)


@app.route('/tables/<table>', methods=['POST', 'GET'])
@stuff.login_and_role_required(current_user, '/tables/')
def tables(table):
    if request.method == 'GET':
        return render_template(f'{table}.html', sort='id', reverse=0, user=current_user)
    elif request.method == 'POST':
        stuff.update_entry(table, request.form)
        return redirect(f'/tables/{table}')


@app.route('/tables/workers/<int:worker_id>', methods=['GET', 'POST'])
@stuff.login_and_role_required(current_user, '/tables/worker')
def user(worker_id):
    if request.method == 'GET':
        return render_template('worker.html', user=current_user,
                               this_user=stuff.get_entry('workers', worker_id))
    elif request.method == 'POST':
        stuff.update_entry('workers', request.form)
        return redirect(f'/tables/workers')


@app.route('/tables/orders/<int:order_id>', methods=['GET', 'POST'])
@stuff.login_and_role_required(current_user, '/tables/order')
def order(order_id):
    if request.method == 'GET':
        return render_template('order.html', user=current_user,
                               order=stuff.get_entry('orders', order_id))
    elif request.method == 'POST':
        stuff.update_entry('orders', request.form)
        return redirect(f'/tables/orders')


@app.route('/tables/<table>/<int:entry_id>/delete', methods=['GET', 'POST'])
@stuff.login_and_role_required(current_user, '/tables/delete')
def delete_entry(table, entry_id):
    stuff.delete_entry(table, entry_id)
    return redirect(f'/tables/{table}')


@app.route('/tables/clients/<int:client_id>', methods=['GET', 'POST'])
@stuff.login_and_role_required(current_user, '/tables/client')
def client(client_id):
    if request.method == 'GET':
        return render_template('client.html', user=current_user,
                               client=stuff.get_entry('clients', client_id))
    elif request.method == 'POST':
        stuff.update_entry('clients', request.form)
        return redirect(f'/tables/clients')


@app.route('/tables/acceptances/<int:acceptance_id>', methods=['GET', 'POST'])
@stuff.login_and_role_required(current_user, '/tables/acceptance')
def acceptance(acceptance_id):
    if request.method == 'GET':
        data = stuff.get_entry('acceptances', acceptance_id)
        things = stuff.get_table('things').filter(Thing.id.in_(loads(data.things)))
        resp = make_response(render_template('acceptance.html', user=current_user,
                                             acceptance=data, things=things))
        resp.set_cookie('acceptance', str(acceptance_id))
        return resp
    elif request.method == 'POST':
        stuff.update_entry('acceptances', request.form)
        return redirect(f'/tables/acceptances')


@app.route('/tables/acceptances/new/<int:order_id>')
@stuff.login_and_role_required(current_user, '/tables/acceptance/new')
def new_acceptance(order_id):
    acceptance_id = stuff.create_acceptance(order_id)
    return redirect(f'/tables/acceptances/{acceptance_id}')


@app.route('/tables/acceptances/<int:acceptance_id>/remove_thing/<int:thing_id>')
@stuff.login_and_role_required(current_user, '/tables/acceptance/remove_thing')
def remove_thing(acceptance_id, thing_id):
    stuff.remove_thing_from_acceptance(acceptance_id, thing_id)
    return redirect(f'/tables/acceptances/{acceptance_id}')


@app.route('/tables/acceptances/<acceptance_id>/add_thing/<int:thing_id>')
@stuff.login_and_role_required(current_user, '/tables/acceptance/add_thing')
def add_thing(acceptance_id, thing_id):
    stuff.add_thing_to_acceptance(acceptance_id, thing_id)
    return redirect(f'/tables/acceptances/{acceptance_id}')


@app.route('/tables/things/<int:thing_id>', methods=['GET', 'POST'])
@stuff.login_and_role_required(current_user, '/tables/thing')
def thing(thing_id):
    if request.method == 'GET':
        acceptance = stuff.get_entry('acceptances', int(request.cookies.get('acceptance'))) \
            if request.cookies.get('acceptance') else None
        return render_template(f'thing.html', user=current_user,
                               acceptance=acceptance,
                               thing=stuff.get_entry('things', thing_id))
    elif request.method == 'POST':
        stuff.update_entry('things', request.form)
        return redirect(f'/tables/things')


@app.route('/tables/things/<int:thing_id>/qr')
@stuff.login_and_role_required(current_user, '/tables/thing/qr')
def thing_qr(thing_id):
    return send_file(stuff.create_qr(f'/tables/things/{thing_id}'), mimetype='image/png')


@app.route('/tables/works/<int:work_id>', methods=['GET', 'POST'])
@stuff.login_and_role_required(current_user, '/tables/work')
def work(work_id):
    if request.method == 'GET':
        return render_template(f'work.html', user=current_user, work=stuff.get_entry('works', work_id))
    elif request.method == 'POST':
        stuff.update_entry('works', request.form)
        return redirect(f'/tables/works')


@app.route('/tables/works/new/<int:thing_id>')
@stuff.login_and_role_required(current_user, '/tables/work/new')
def new_work(thing_id):
    created_work = stuff.create_work(thing_id, current_user)
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
    db_session.global_init("db/data.db")
    stuff.db_sess = db_session.create_session()
    api.add_resource(restful_resources.ClientsListResource, '/api/clients')
    api.add_resource(restful_resources.ClientsResource, '/api/clients/<int:client_id>')
    api.add_resource(restful_resources.AcceptancesListResource, '/api/acceptances')
    api.add_resource(restful_resources.AcceptancesResource, '/api/acceptances/<int:acceptance_id>')
    api.add_resource(restful_resources.ThingsListResource, '/api/thing')
    api.add_resource(restful_resources.ThingsResource, '/api/things/<int:thing_id>')
    api.add_resource(restful_resources.WorkersListResource, '/api/workers')
    api.add_resource(restful_resources.WorkersResource, '/api/workers/<int:worker_id>')
    api.add_resource(restful_resources.WorksListResource, '/api/works')
    api.add_resource(restful_resources.WorksResource, '/api/works/<int:work_id>')
    api.add_resource(restful_resources.OrdersListResource, '/api/orders')
    api.add_resource(restful_resources.OrdersResource, '/api/orders/<int:order_id>')
    app.run(port=8080, host='0.0.0.0')


if __name__ == '__main__':
    main()
