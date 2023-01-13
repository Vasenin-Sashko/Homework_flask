import requests

# responce = requests.post('http://127.0.0.1:5000/advs',
#                         json={'id': '1',
#                               'heading': 'Car',
#                               'description': 'Good Car',
#                               'user_name': 'Alex'},
#                         )
# print(responce.status_code)
# print(responce.json())
#
responce = requests.delete('http://127.0.0.1:5000/advs/1')
print(responce.status_code)
print(responce.json())

responce = requests.get('http://127.0.0.1:5000/advs/1')
print(responce.status_code)
print(responce.json())


