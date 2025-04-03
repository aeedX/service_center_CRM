import sqlite3
from io import BytesIO

from qrcode.constants import ERROR_CORRECT_H
from qrcode.main import QRCode

def create_qr(data):
    qr = QRCode(error_correction=ERROR_CORRECT_H)
    qr.add_data(data)
    img = qr.make_image()
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    return img_io

def check_user(user):
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    result = cursor.execute("""SELECT user, password FROM users WHERE user = ?""", (user,)).fetchall()

    connection.close()
    return result
