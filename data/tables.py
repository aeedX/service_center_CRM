import datetime as dt
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, orm
from data import db_session

from werkzeug.security import generate_password_hash, check_password_hash


class Client(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'clients'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.String, nullable=True, default='')
    address = Column(sqlalchemy.String, nullable=True, default='')
    phone = Column(sqlalchemy.String, nullable=True, default='')
    comment = Column(sqlalchemy.String, nullable=True, default='')

    orders = orm.relationship('Order', back_populates='client')
    things = orm.relationship('Thing', back_populates='client')


class Order(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    client_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('clients.id'))
    create_date = Column(sqlalchemy.Date, default=dt.date.today())
    comment = Column(sqlalchemy.String, nullable=True, default='')
    status =  Column(sqlalchemy.String, nullable=True, default='created')

    client = orm.relationship('Client')
    acceptances = orm.relationship('Acceptance', back_populates='order')


class Acceptance(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'acceptances'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    order_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('orders.id'))
    worker_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('workers.id'))
    things =  Column(sqlalchemy.String, default='[]', nullable=True)
    comment = Column(sqlalchemy.String, nullable=True, default='')
    status =  Column(sqlalchemy.String, nullable=True, default='taken from client')

    order = orm.relationship('Order')
    worker = orm.relationship('Worker')
    works = orm.relationship('Work', back_populates='acceptance')


class Thing(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'things'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sn =  Column(sqlalchemy.String, nullable=True, unique=True)
    vendor = Column(sqlalchemy.String, nullable=True)
    model = Column(sqlalchemy.String, nullable=True)
    client_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('clients.id'))
    comment = Column(sqlalchemy.String, nullable=True)

    client = orm.relationship('Client')
    works = orm.relationship('Work', back_populates='thing')


class Work(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'works'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    acceptance_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('acceptances.id'))
    thing_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('things.id'))
    worker_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('workers.id'))
    date = Column(sqlalchemy.Date, default=dt.date.today())
    actions =  Column(sqlalchemy.String, nullable=True, default='')
    comment = Column(sqlalchemy.String, nullable=True)
    status =  Column(sqlalchemy.String, nullable=True)

    acceptance = orm.relationship('Acceptance')
    thing = orm.relationship('Thing')
    worker = orm.relationship('Worker')


class Worker(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'workers'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = Column(sqlalchemy.String, nullable=True)
    name = Column(sqlalchemy.String, nullable=True)
    password = Column(sqlalchemy.String, nullable=True)
    role = Column(sqlalchemy.String, nullable=True)
    phone = Column(sqlalchemy.String, nullable=True)
    comment = Column(sqlalchemy.String, nullable=True)

    works = orm.relationship('Work', back_populates='worker')
    acceptances = orm.relationship('Acceptance', back_populates='worker')


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)
