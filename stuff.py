from io import BytesIO
from json import loads, dumps
import datetime as dt

from qrcode.constants import ERROR_CORRECT_H
from qrcode.main import QRCode

from data.tables import *


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
    if acceptances:
        work.acceptance_id = acceptances[0].id
        db_sess.add(work)
        db_sess.commit()
        #return work
        return list(db_sess.query(Work))[-1]


def create_acceptance(order_id):
    db_sess = db_session.create_session()
    acceptance = Acceptance()
    if order_id != 0:
        acceptance.order_id = order_id
    db_sess.add(acceptance)
    db_sess.commit()
    return list(db_sess.query(Acceptance))[-1].id



def get_user(username):
    db_sess = db_session.create_session()
    worker = db_sess.query(Worker).filter(Worker.username == username).first()
    db_sess.close()
    return worker


def get_table(table, sort='id', reverse=0):
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
        return db_sess.query(Order).get(id)
    elif table == 'acceptances':
        return db_sess.query(Acceptance).filter(Acceptance.id == id).first()
    elif table == 'things':
        return db_sess.query(Thing).filter(Thing.id == id).first()
    elif table == 'works':
        return db_sess.query(Work).filter(Work.id == id).first()
    elif table == 'workers':
        return db_sess.query(Worker).filter(Worker.id == id).first()
    db_sess.close()


def delete_entry(table, entry_id):
    db_sess = db_session.create_session()
    if table == 'clients':
        db_sess.delete(db_sess.query(Client).get(entry_id))
    elif table == 'orders':
        db_sess.delete(db_sess.query(Order).get(entry_id))
    elif table == 'acceptances':
        db_sess.delete(db_sess.query(Acceptance).get(entry_id))
    elif table == 'things':
        db_sess.delete(db_sess.query(Thing).get(entry_id))
    elif table == 'works':
        db_sess.delete(db_sess.query(Work).get(entry_id))
    elif table == 'workers':
        db_sess.delete(db_sess.query(Worker).get(entry_id))
    db_sess.commit()


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
                                                     '%Y-%m-%d') if form['date'] else entry.create_date
            entry.comment = form['comment'] if form['comment'] else entry.comment
            entry.status = form['status'] if form['status'] else entry.status
        else:
            entry = Order()
            entry.client_id = int(form['client']) if form['client'] else None
            entry.create_date = dt.datetime.strptime(form['date'],
                                                     '%Y-%m-%d') if form['date'] else dt.datetime.now()
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
            entry = db_sess.query(Thing).get(form['id'])
            entry.sn = form['sn']
            entry.vendor = form['vendor']
            entry.model = form['model']
            entry.client_id = form['client']
            entry.comment = form['comment']
        else:
            entry = Thing()
            entry.sn = form['sn']
            entry.vendor = form['vendor']
            entry.model = form['model']
            entry.client_id = form['client']
            entry.comment = form['comment']
    elif table == 'works':
        entry = db_sess.query(Work).filter(Work.id == form['id']).first()
        entry.comment = form['comment']
        entry.actions = ' '.join(form.getlist('actions'))
    elif table == 'users':
        if form['id']:
            entry = db_sess.query(Worker).get(form['id'])
            entry.username = form['username']
            entry.name = form['name']
            if form['new_password']:
                entry.set_password(form['new_password'])
            entry.role = form['role']
            entry.phone = form['phone']
            entry.comment = form['comment']
        else:
            entry = Worker()
            entry.username = form['username']
            entry.name = form['name']
            entry.set_password(form['password'])
            entry.role = form['role']
            entry.phone = form['phone']
            entry.comment = form['comment']
    if not form['id']:
        db_sess.add(entry)
    db_sess.commit()


def remove_thing_from_acceptance(acceptance_id, thing_id):
    db_sess = db_session.create_session()
    acceptance = db_sess.query(Acceptance).get(acceptance_id)
    things = list(loads(acceptance.things))
    if thing_id in things:
        things.remove(thing_id)
        acceptance.things = dumps(things)
        db_sess.commit()


def add_thing_to_acceptance(acceptance_id, thing_id):
    db_sess = db_session.create_session()
    acceptance = db_sess.query(Acceptance).get(acceptance_id)
    things = list(loads(acceptance.things))
    if thing_id not in things:
        things.append(thing_id)
        acceptance.things = dumps(things)
        db_sess.commit()
