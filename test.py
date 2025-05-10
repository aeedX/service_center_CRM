from requests import get, post, delete

print(get('http://127.0.0.1:8080/api/order').json())

print(get('http://127.0.0.1:8080/api/order/1').json())

print(get('http://127.0.0.1:8080/api/order/999').json())

print(get('http://127.0.0.1:8080/api/order/q').json())

print(post('http://127.0.0.1:8080/api/order', json={}).json())

print(post('http://127.0.0.1:8080/api/order',
           json={'name': 'Заголовок'}).json())

print(post('http://127.0.0.1:8080/api/order',
           json={'client_id': 1,
                 'create_date': '2025-04-26 10:55:33.902342',
                 'comment': 'sd',
                 'status': 'created'}).json())

print(delete('http://127.0.0.1:8080/api/order/999').json())
# новости с id = 999 нет в базе

print(delete('http://127.0.0.1:8080/api/order/4').json())