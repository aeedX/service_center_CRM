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


def get_user(username):
    db_sess = db_session.create_session()
    worker = db_sess.query(Worker).filter(Worker.username == username).first()
    db_sess.close()
    return worker


def get_table(table, sort, reverse):
    db_sess = db_session.create_session()
    if table == 'clients':
        return [(data.id, data.name, data.address, data.phone, data.comment) for data in db_sess.query(Client)]
    elif table == 'orders':
        return [(data.id, db_sess.query(Client).filter(Client.id == data.client_id).first().name,
                 data.create_date, data.comment, data.status) for data in db_sess.query(Order)]
    elif table == 'acceptances':
        return [(data.id, data.order_id, db_sess.query(Worker).filter(Worker.id == data.worker_id).first().name,
                 data.things, data.comment, data.status) for data in db_sess.query(Acceptance)]
    elif table == 'things':
        return [(data.id, data.name, data.address, data.phone, data.comment) for data in db_sess.query(Thing)]
    elif table == 'shipments':
        return [(data.id, data.name, data.address, data.phone, data.comment) for data in db_sess.query(Shipment)]
    elif table == 'works':
        return [(data.id, data.name, data.address, data.phone, data.comment) for data in db_sess.query(Work)]
    elif table == 'workers':
        return [(data.id, data.name, data.address, data.phone, data.comment) for data in db_sess.query(Worker)]
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
    elif table == 'shipments':
        return db_sess.query(Shipment).filter(Shipment.id == id).first()
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
        if form['id'] and (form['client'] and form['client'].isdigit() or not form['client']):
            entry = db_sess.query(Order).filter(Order.id == form['id']).first()
            entry.client_id = int(form['client']) if form['client'] else entry.client_id
            entry.create_date = dt.datetime.strptime(form['date'],
                                                     '%Y-%m-%d %H:%M:%S.%f') if form['date'] else entry.create_date
            entry.comment = form['comment'] if form['comment'] else entry.comment
            entry.status = form['status'] if form['status'] else entry.status
        elif form['client'] and form['client'].isdigit():
            entry = Order()
            entry.client_id = int(form['client'])
            entry.create_date = dt.datetime.strptime(form['date'],
                                                     '%Y-%m-%d %H:%M:%S.%f') if form['date'] else dt.datetime.now()
            entry.comment = form['comment']
            entry.status = form['status'] if form['status'] else 'created'
        else:
            return
    elif table == 'acceptances':
        if form['id']:
            entry = db_sess.query(Acceptance).filter(Acceptance.id == form['id']).first()
            entry.order_id = int(form['order']) if form['order'] else entry.order_id
            entry.worker_id = int(form['worker']) if form['worker'] else entry.worker_id
            entry.things = form['things'] if form['things'] else entry.things
            entry.comment = form['comment'] if form['comment'] else entry.comment
            entry.status = form['status'] if form['status'] else entry.status
        elif form['order'] and form['worker']:
            entry = Order()
            entry.order_id = int(form['order'])
            entry.worker_id = int(form['worker'])
            entry.things = form['things']
            entry.comment = form['comment']
            entry.status = form['status'] if form['status'] else 'created'
        else:
            return
    elif table == 'things':
        pass
    elif table == 'shipments':
        pass
    elif table == 'works':
        pass
    elif table == 'workers':
        pass
    if not form['id']:
        db_sess.add(entry)
    db_sess.commit()
