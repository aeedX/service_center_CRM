import datetime as dt
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, orm
from data import db_session


class Client(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'clients'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.String, nullable=True)
    address = Column(sqlalchemy.String, nullable=True)
    phone = Column(sqlalchemy.String, nullable=True)
    comment = Column(sqlalchemy.String, nullable=True)


class Order(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    client_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('clients.id'))
    create_date = Column(sqlalchemy.DateTime, default=dt.datetime.now())
    comment = Column(sqlalchemy.String, nullable=True)
    status =  Column(sqlalchemy.String, nullable=True)

    client = orm.relationship('Client')


class Acceptance(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'acceptances'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    order_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('orders.id'))
    worker_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('workers.id'))
    things =  Column(sqlalchemy.String, default='[]', nullable=True)
    comment = Column(sqlalchemy.String, nullable=True)
    status =  Column(sqlalchemy.String, nullable=True)

    order = orm.relationship('Order')
    worker = orm.relationship('Worker')


class Thing(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'things'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    sn =  Column(sqlalchemy.String, nullable=True)
    vendor = Column(sqlalchemy.String, nullable=True)
    model = Column(sqlalchemy.String, nullable=True)
    client_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('clients.id'))
    comment = Column(sqlalchemy.String, nullable=True)

    client = orm.relationship('Client')


class Work(db_session.SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'works'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    acceptance_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('acceptances.id'))
    thing_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('things.id'))
    worker_id = Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('workers.id'))
    actions =  Column(sqlalchemy.String, nullable=True)
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
