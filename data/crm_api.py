import flask

from data import db_session
from .tables import Client, Acceptance, Thing, Worker, Work, Order
from flask import jsonify, make_response, request

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


# client

@blueprint.route('/api/client')
def get_clients():
    db_sess = db_session.create_session()
    client = db_sess.query(Client).all()
    return jsonify(
        {
            'clients':
                [item.to_dict(only=('name', 'address', 'phone', 'comment'))
                 for item in client]
        }
    )


@blueprint.route('/api/client/<int:client_id>', methods=['GET'])
def get_one_clients(client_id):
    db_sess = db_session.create_session()
    clients = db_sess.query(Client).get(client_id)
    if not clients:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'client': clients.to_dict(only=(
                'name', 'address', 'phone', 'comment'))
        }
    )


@blueprint.route('/api/client', methods=['POST'])
def create_clients():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['name', 'address', 'phone', 'comment']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    clients = Client(
        name=request.json['name'],
        address=request.json['address'],
        phone=request.json['phone'],
        comment=request.json['comment']
    )
    db_sess.add(clients)
    db_sess.commit()
    return jsonify({'id': clients.id})


@blueprint.route('/api/client/<int:client_id>', methods=['DELETE'])
def delete_clients(client_id):
    db_sess = db_session.create_session()
    clients = db_sess.query(Client).get(client_id)
    if not clients:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(clients)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# acceptance

@blueprint.route('/api/acceptance')
def get_acceptances():
    db_sess = db_session.create_session()
    acceptance = db_sess.query(Acceptance).all()
    return jsonify(
        {
            'acceptances':
                [item.to_dict(only=('order_id', 'worker_id', 'things', 'comment', 'status'))
                 for item in acceptance]
        }
    )


@blueprint.route('/api/acceptance/<int:acceptance_id>', methods=['GET'])
def get_one_acceptances(acceptance_id):
    db_sess = db_session.create_session()
    acceptances = db_sess.query(Acceptance).get(acceptance_id)
    if not acceptances:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'acceptance': acceptances.to_dict(only=(
                'order_id', 'worker_id', 'things', 'comment', 'status'))
        }
    )


@blueprint.route('/api/acceptance', methods=['POST'])
def create_acceptances():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['order_id', 'worker_id', 'things', 'comment', 'status']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    acceptances = Acceptance(
        order_id=request.json['order_id'],
        worker_id=request.json['worker_id'],
        things=request.json['things'],
        comment=request.json['comment'],
        status=request.json['status']
    )
    db_sess.add(acceptances)
    db_sess.commit()
    return jsonify({'id': acceptances.id})


@blueprint.route('/api/acceptance/<int:acceptance_id>', methods=['DELETE'])
def delete_acceptances(acceptance_id):
    db_sess = db_session.create_session()
    acceptances = db_sess.query(Acceptance).get(acceptance_id)
    if not acceptances:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(acceptances)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# thing

@blueprint.route('/api/thing')
def get_things():
    db_sess = db_session.create_session()
    thing = db_sess.query(Thing).all()
    return jsonify(
        {
            'things':
                [item.to_dict(only=('sn', 'vendor', 'model', 'client_id', 'comment'))
                 for item in thing]
        }
    )


@blueprint.route('/api/thing/<int:thing_id>', methods=['GET'])
def get_one_things(thing_id):
    db_sess = db_session.create_session()
    things = db_sess.query(Thing).get(thing_id)
    if not things:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'thing': things.to_dict(only=(
                'sn', 'vendor', 'model', 'client_id', 'comment'))
        }
    )


@blueprint.route('/api/thing', methods=['POST'])
def create_things():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['sn', 'vendor', 'model', 'client_id', 'comment']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    things = Thing(
        sn=request.json['sn'],
        vendor=request.json['vendor'],
        model=request.json['model'],
        comment=request.json['comment'],
        client_id=request.json['client_id']
    )
    db_sess.add(things)
    db_sess.commit()
    return jsonify({'id': things.id})


@blueprint.route('/api/thing/<int:thing_id>', methods=['DELETE'])
def delete_things(thing_id):
    db_sess = db_session.create_session()
    things = db_sess.query(Thing).get(thing_id)
    if not things:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(things)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# worker

@blueprint.route('/api/worker')
def get_workers():
    db_sess = db_session.create_session()
    worker = db_sess.query(Worker).all()
    return jsonify(
        {
            'workers':
                [item.to_dict(only=('username', 'name', 'password', 'role', 'phone', 'comment'))
                 for item in worker]
        }
    )


@blueprint.route('/api/worker/<int:worker_id>', methods=['GET'])
def get_one_workers(worker_id):
    db_sess = db_session.create_session()
    workers = db_sess.query(Worker).get(worker_id)
    if not workers:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'worker': workers.to_dict(only=(
                'username', 'name', 'password', 'role', 'phone', 'comment'))
        }
    )


@blueprint.route('/api/worker', methods=['POST'])
def create_workers():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['username', 'name', 'password', 'role', 'phone', 'comment']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    workers = Worker(
        username=request.json['username'],
        name=request.json['name'],
        password=request.json['password'],
        comment=request.json['comment'],
        phone=request.json['phone'],
        role=request.json['role']
    )
    db_sess.add(workers)
    db_sess.commit()
    return jsonify({'id': workers.id})


@blueprint.route('/api/worker/<int:worker_id>', methods=['DELETE'])
def delete_workers(worker_id):
    db_sess = db_session.create_session()
    workers = db_sess.query(Worker).get(worker_id)
    if not workers:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(workers)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# work

@blueprint.route('/api/work')
def get_works():
    db_sess = db_session.create_session()
    work = db_sess.query(Work).all()
    return jsonify(
        {
            'works':
                [item.to_dict(only=('acceptance_id', 'thing_id', 'worker_id', 'actions', 'status', 'comment'))
                 for item in work]
        }
    )


@blueprint.route('/api/work/<int:work_id>', methods=['GET'])
def get_one_works(work_id):
    db_sess = db_session.create_session()
    works = db_sess.query(Work).get(work_id)
    if not works:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'work': works.to_dict(only=(
                'acceptance_id', 'thing_id', 'worker_id', 'actions', 'status', 'comment'))
        }
    )


@blueprint.route('/api/work', methods=['POST'])
def create_works():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['acceptance_id', 'thing_id', 'worker_id', 'actions', 'status', 'comment']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    works = Work(
        acceptance_id=request.json['acceptance_id'],
        thing_id=request.json['thing_id'],
        worker_id=request.json['worker_id'],
        actions=request.json['actions'],
        status=request.json['status'],
        comment=request.json['comment']
    )
    db_sess.add(works)
    db_sess.commit()
    return jsonify({'id': works.id})


@blueprint.route('/api/work/<int:work_id>', methods=['DELETE'])
def delete_works(work_id):
    db_sess = db_session.create_session()
    works = db_sess.query(Work).get(work_id)
    if not works:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(works)
    db_sess.commit()
    return jsonify({'success': 'OK'})


# order

@blueprint.route('/api/order')
def get_orders():
    db_sess = db_session.create_session()
    order = db_sess.query(Order).all()
    return jsonify(
        {
            'orders':
                [item.to_dict(only=('client_id', 'create_date', 'comment', 'status'))
                 for item in order]
        }
    )


@blueprint.route('/api/order/<int:order_id>', methods=['GET'])
def get_one_orders(order_id):
    db_sess = db_session.create_session()
    orders = db_sess.query(Order).get(order_id)
    if not orders:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'order': orders.to_dict(only=(
                'client_id', 'create_date', 'comment', 'status'))
        }
    )


@blueprint.route('/api/order', methods=['POST'])
def create_orders():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['client_id', 'create_date', 'comment', 'status']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    orders = Order(
        client_id=request.json['client_id'],
        create_date=request.json['create_date'],
        comment=request.json['comment'],
        status=request.json['status']
    )
    db_sess.add(orders)
    db_sess.commit()
    return jsonify({'id': orders.id})


@blueprint.route('/api/order/<int:order_id>', methods=['DELETE'])
def delete_orders(order_id):
    db_sess = db_session.create_session()
    order = db_sess.query(Order).get(order_id)
    if not order:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(order)
    db_sess.commit()
    return jsonify({'success': 'OK'})
