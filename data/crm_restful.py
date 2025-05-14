import flask
from flask import Flask
from data import db_session
from flask_restful import reqparse, abort, Api, Resource
from .tables import Client, Acceptance, Thing, Worker, Work, Order
from flask import jsonify, make_response, request


app = Flask(__name__)
api = Api(app)


def abort_if_anything_not_found(id, thing):
    session = db_session.create_session()
    things = session.query(thing).get(id)
    if not things:
        abort(404, message=f"{(str(thing.__tablename__)[:-1]).capitalize()} {id} not found")

# client

class ClientResource(Resource):
    def get(self, client_id):
        abort_if_anything_not_found(client_id, Client)
        session = db_session.create_session()
        clients = session.query(Client).get(client_id)
        return jsonify({'client': clients.to_dict(
            only=('name', 'address', 'phone', 'comment'))})

    def delete(self, client_id):
        abort_if_anything_not_found(client_id, Client)
        session = db_session.create_session()
        clients = session.query(Client).get(client_id)
        session.delete(clients)
        session.commit()
        return jsonify({'success': 'OK'})

parser_c = reqparse.RequestParser()
parser_c.add_argument('name', required=True)
parser_c.add_argument('address', required=True)
parser_c.add_argument('phone', required=True)
parser_c.add_argument('comment', required=True)

class ClientListResource(Resource):
    def get(self):
        session = db_session.create_session()
        clients = session.query(Client).all()
        return jsonify({'clients': [item.to_dict(
            only=('name', 'address', 'phone', 'comment')) for item in clients]})

    def post(self):
        args = parser_c.parse_args()
        session = db_session.create_session()
        clients = Client(
            name=args['name'],
            address=args['address'],
            phone=args['phone'],
            comment=args['comment']
        )
        session.add(clients)
        session.commit()
        return jsonify({'id': clients.id})

# acceptance

class AcceptanceResource(Resource):
    def get(self, acceptance_id):
        abort_if_anything_not_found(acceptance_id, Acceptance)
        session = db_session.create_session()
        acceptances = session.query(Acceptance).get(acceptance_id)
        return jsonify({'acceptance': acceptances.to_dict(
            only=('order_id', 'worker_id', 'things', 'comment', 'status'))})

    def delete(self, acceptance_id):
        abort_if_anything_not_found(acceptance_id, Acceptance)
        session = db_session.create_session()
        acceptances = session.query(Acceptance).get(acceptance_id)
        session.delete(acceptances)
        session.commit()
        return jsonify({'success': 'OK'})

parser_a = reqparse.RequestParser()
parser_a.add_argument('order_id', required=True)
parser_a.add_argument('worker_id', required=True)
parser_a.add_argument('things', required=True)
parser_a.add_argument('comment', required=True)
parser_a.add_argument('status', required=True)

class AcceptanceListResource(Resource):
    def get(self):
        session = db_session.create_session()
        acceptances = session.query(Acceptance).all()
        return jsonify({'acceptances': [item.to_dict(
            only=('order_id', 'worker_id', 'things', 'comment', 'status')) for item in acceptances]})

    def post(self):
        args = parser_a.parse_args()
        session = db_session.create_session()
        acceptances = Acceptance(
            order_id=args['order_id'],
            worker_id=args['worker_id'],
            things=args['things'],
            comment=args['comment'],
            status=args['status']
        )
        session.add(acceptances)
        session.commit()
        return jsonify({'id': acceptances.id})

# thing

class ThingResource(Resource):
    def get(self, thing_id):
        abort_if_anything_not_found(thing_id, Thing)
        session = db_session.create_session()
        things = session.query(Thing).get(thing_id)
        return jsonify({'thing': things.to_dict(
            only=('sn', 'vendor', 'model', 'client_id', 'comment'))})

    def delete(self, thing_id):
        abort_if_anything_not_found(thing_id, Thing)
        session = db_session.create_session()
        things = session.query(Thing).get(thing_id)
        session.delete(things)
        session.commit()
        return jsonify({'success': 'OK'})

parser_th = reqparse.RequestParser()
parser_th.add_argument('sn', required=True)
parser_th.add_argument('vendor', required=True)
parser_th.add_argument('model', required=True)
parser_th.add_argument('client_id', required=True)
parser_th.add_argument('comment', required=True)

class ThingListResource(Resource):
    def get(self):
        session = db_session.create_session()
        things = session.query(Thing).all()
        return jsonify({'things': [item.to_dict(
            only=('sn', 'vendor', 'model', 'client_id', 'comment')) for item in things]})

    def post(self):
        args = parser_th.parse_args()
        session = db_session.create_session()
        things = Thing(
            sn=args['sn'],
            vendor=args['vendor'],
            model=args['model'],
            client_id=args['client_id'],
            comment=args['comment']
        )
        session.add(things)
        session.commit()
        return jsonify({'id': things.id})

# worker

class WorkerResource(Resource):
    def get(self, worker_id):
        abort_if_anything_not_found(worker_id, Worker)
        session = db_session.create_session()
        workers = session.query(Worker).get(worker_id)
        return jsonify({'worker': workers.to_dict(
            only=('username', 'name', 'password', 'role', 'phone', 'comment'))})

    def delete(self, worker_id):
        abort_if_anything_not_found(worker_id, Worker)
        session = db_session.create_session()
        workers = session.query(Worker).get(worker_id)
        session.delete(workers)
        session.commit()
        return jsonify({'success': 'OK'})

parser_worker = reqparse.RequestParser()
parser_worker.add_argument('username', required=True)
parser_worker.add_argument('name', required=True)
parser_worker.add_argument('password', required=True)
parser_worker.add_argument('role', required=True)
parser_worker.add_argument('phone', required=True)
parser_worker.add_argument('comment', required=True)

class WorkerListResource(Resource):
    def get(self):
        session = db_session.create_session()
        workers = session.query(Worker).all()
        return jsonify({'workers': [item.to_dict(
            only=('username', 'name', 'password', 'role', 'phone', 'comment')) for item in workers]})

    def post(self):
        args = parser_worker.parse_args()
        session = db_session.create_session()
        workers = Worker(
            username=args['username'],
            name=args['name'],
            password=args['password'],
            role=args['role'],
            phone=args['phone'],
            comment=args['comment']
        )
        session.add(workers)
        session.commit()
        return jsonify({'id': workers.id})

# work

class WorkResource(Resource):
    def get(self, work_id):
        abort_if_anything_not_found(work_id, Work)
        session = db_session.create_session()
        works = session.query(Work).get(work_id)
        return jsonify({'work': works.to_dict(
            only=('acceptance_id', 'thing_id', 'worker_id', 'actions', 'status', 'comment'))})

    def delete(self, work_id):
        abort_if_anything_not_found(work_id, Work)
        session = db_session.create_session()
        works = session.query(Work).get(work_id)
        session.delete(works)
        session.commit()
        return jsonify({'success': 'OK'})

parser_work = reqparse.RequestParser()
parser_work.add_argument('acceptance_id', required=True)
parser_work.add_argument('thing_id', required=True)
parser_work.add_argument('worker_id', required=True)
parser_work.add_argument('actions', required=True)
parser_work.add_argument('status', required=True)
parser_work.add_argument('comment', required=True)

class WorkListResource(Resource):
    def get(self):
        session = db_session.create_session()
        works = session.query(Work).all()
        return jsonify({'works': [item.to_dict(
            only=('acceptance_id', 'thing_id', 'worker_id', 'actions', 'status', 'comment')) for item in works]})

    def post(self):
        args = parser_work.parse_args()
        session = db_session.create_session()
        works = Work(
            acceptance_id=args['acceptance_id'],
            thing_id=args['thing_id'],
            worker_id=args['worker_id'],
            actions=args['actions'],
            status=args['status'],
            comment=args['comment']
        )
        session.add(works)
        session.commit()
        return jsonify({'id': works.id})

# order

class OrderResource(Resource):
    def get(self, order_id):
        abort_if_anything_not_found(order_id, Order)
        session = db_session.create_session()
        orders = session.query(Order).get(order_id)
        return jsonify({'order': orders.to_dict(
            only=('client_id', 'create_date', 'comment', 'status'))})

    def delete(self, order_id):
        abort_if_anything_not_found(order_id, Order)
        session = db_session.create_session()
        orders = session.query(Order).get(order_id)
        session.delete(orders)
        session.commit()
        return jsonify({'success': 'OK'})

parser_order = reqparse.RequestParser()
parser_order.add_argument('client_id', required=True)
parser_order.add_argument('create_date')
parser_order.add_argument('status', required=True)
parser_order.add_argument('comment', required=True)

class OrderListResource(Resource):
    def get(self):
        session = db_session.create_session()
        orders = session.query(Order).all()
        return jsonify({'orders': [item.to_dict(
            only=('client_id', 'create_date', 'comment', 'status')) for item in orders]})

    def post(self):
        args = parser_order.parse_args()
        session = db_session.create_session()
        orders = Order(
            client_id=args['client_id'],
            create_date=args['create_date'],
            comment=args['comment'],
            status=args['status']

        )
        session.add(orders)
        session.commit()
        return jsonify({'id': orders.id})



