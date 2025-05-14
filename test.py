from requests import get, post, delete

print(get('http://127.0.0.1:8080/api/order').json())

print(get('http://127.0.0.1:8080/api/order/2').json())

print(get('http://127.0.0.1:8080/api/order/999').json())

print(get('http://127.0.0.1:8080/api/order/q').json())

print(post('http://127.0.0.1:8080/api/order', json={}).json())

print(post('http://127.0.0.1:8080/api/order',
           json={'name': 'Заголовок'}).json())

print(post('http://127.0.0.1:8080/api/order',
           json={'client_id': 1,
                 'comment': 'sd',
                 'status': 'created'}).json())

print(delete('http://127.0.0.1:8080/api/order/6').json())
# новости с id = 999 нет в базе

print(delete('http://127.0.0.1:8080/api/order/222222').json())