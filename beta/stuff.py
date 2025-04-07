import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from data import db_session
from data.tables import Worker

from io import BytesIO

from qrcode.constants import ERROR_CORRECT_H
from qrcode.main import QRCode

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

def check_user(user):
    db_session.global_init('db/data.db')
    db_sess = db_session.create_session()
    print(user)
    user = db_sess.query(Worker).filter(Worker.password == user).first()
    return user
