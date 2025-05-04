from io import BytesIO
import datetime as dt

from qrcode.constants import ERROR_CORRECT_H
from qrcode.main import QRCode

from data.tables import *

SqlAlchemyBase = orm.declarative_base()

__factory = None


def create_qr(data):
    qr = QRCode(error_correction=ERROR_CORRECT_H)
    qr.add_data(data)
    img = qr.make_image()
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io


def create_work(thing_id, user):
    db_sess = db_session.create_session()
    work = Work()
    work.thing_id = thing_id
    work.worker_id = user.id
    acceptances = [data for data in db_sess.query(Acceptance) if data.status == 'delivered to the worker' and
                   str(thing_id) in data.things.split() and data.worker_id == user.id]
    work.actions = ''
    if acceptances:
        work.acceptance_id = acceptances[0].id
        db_sess.add(work)
        db_sess.commit()
        #return work
        return list(db_sess.query(Work))[-1]


def get_user(username):
    db_sess = db_session.create_session()
    worker = db_sess.query(Worker).filter(Worker.username == username).first()
    db_sess.close()
    return worker


def get_table(table, sort, reverse):
    db_sess = db_session.create_session()
    if table == 'clients':
        return db_sess.query(Client)
    elif table == 'orders':
        return db_sess.query(Order)
    elif table == 'acceptances':
        return db_sess.query(Acceptance)
    elif table == 'things':
        return db_sess.query(Thing)
    elif table == 'works':
        return db_sess.query(Work)
    elif table == 'workers':
        return db_sess.query(Worker)
    db_sess.close()


def get_entry(table, id):
    db_sess = db_session.create_session()
    if table == 'clients':
        return db_sess.query(Client).filter(Client.id == id).first()
    elif table == 'orders':
        entry = db_sess.query(Order).filter(Order.id == id).first()[::]
        entry[1] = db_sess.query(Client).filter(Client.id == entry[1]).first().name
        return entry
    elif table == 'acceptances':
        return db_sess.query(Acceptance).filter(Acceptance.id == id).first()
    elif table == 'things':
        return db_sess.query(Thing).filter(Thing.id == id).first()
    elif table == 'works':
        return db_sess.query(Work).filter(Work.id == id).first()
    elif table == 'workers':
        return db_sess.query(Worker).filter(Worker.id == id).first()
    db_sess.close()


def update_entry(table, form):
    db_sess = db_session.create_session()
    if table == 'clients':
        entry = db_sess.query(Client).filter(Client.id == form['id']).first() if form['id'] else Client()
        entry.name = form['name'] if form['name'] else entry.name
        entry.address = form['address'] if form['address'] else entry.address
        entry.phone = form['phone'] if form['phone'] else entry.phone
        entry.comment = form['comment'] if form['comment'] else entry.comment
    elif table == 'orders':
        if form['id']:
            entry = db_sess.query(Order).filter(Order.id == form['id']).first()
            entry.client_id = int(form['client']) if form['client'] else entry.client_id
            entry.create_date = dt.datetime.strptime(form['date'],
                                                     '%Y-%m-%d %H:%M:%S.%f') if form['date'] else entry.create_date
            entry.comment = form['comment'] if form['comment'] else entry.comment
            entry.status = form['status'] if form['status'] else entry.status
        else:
            entry = Order()
            entry.client_id = int(form['client']) if form['client'] else None
            entry.create_date = dt.datetime.strptime(form['date'],
                                                     '%Y-%m-%d %H:%M:%S.%f') if form['date'] else dt.datetime.now()
            entry.comment = form['comment']
            entry.status = form['status'] if form['status'] else 'created'
    elif table == 'acceptances':
        if form['id']:
            entry = db_sess.query(Acceptance).filter(Acceptance.id == form['id']).first()
            entry.order_id = int(form['order']) if form['order'] else entry.order_id
            entry.worker_id = int(form['worker']) if form['worker'] else entry.worker_id
            entry.things = form['things'] if form['things'] else entry.things
            entry.comment = form['comment'] if form['comment'] else entry.comment
            entry.status = form['status'] if form['status'] else entry.status
        else:
            entry = Order()
            entry.order_id = int(form['order']) if form['order'] else None
            entry.worker_id = int(form['worker']) if form['worker'] else None
            entry.things = form['things']
            entry.comment = form['comment']
            entry.status = form['status'] if form['status'] else 'created'
    elif table == 'things':
        if form['id']:
            entry = db_sess.query(Thing).filter(Thing.id == form['id']).first()
            entry.sn = form['sn'] if form['sn'] else entry.sn
            entry.vendor = form['vendor'] if form['vendor'] else entry.vendor
            entry.model = form['model'] if form['model'] else entry.model
            entry.client_id = int(form['client']) if form['client'] else entry.client_id
            entry.comment = form['comment'] if form['comment'] else entry.comment
        else:
            entry = Thing()
            entry.sn = form['sn']
            entry.vendor = form['vendor']
            entry.model = form['model']
            entry.client_id = int(form['client']) if form['client'] else None
            entry.comment = form['comment']
    elif table == 'works':
        entry = db_sess.query(Work).filter(Work.id == form['id']).first()
        entry.comment = form['comment']
        entry.actions = ' '.join(form.getlist('actions'))
    elif table == 'workers':
        pass
    if not form['id']:
        db_sess.add(entry)
    db_sess.commit()
