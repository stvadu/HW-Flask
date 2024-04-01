import requests

response = requests.post(
    'http://127.0.0.1:5000/ad/',
    json={
        'title': 'Advertisment_1',
        'text': 'Trali-vali-ti-ti-ti',
        'author': 'Author_1',
    },
)
print(response.status_code)
print(response.json())

response = requests.delete(
    'http://127.0.0.1:5000/ad/1',
)
print(response.status_code)
print(response.json())

response = requests.patch(
    'http://127.0.0.1:5000/ad/1',
    json={'text': 'Bred sivoy kabiily'}
)
print(response.status_code)
print(response.json())


response = requests.get(
    'http://127.0.0.1:5000/ad/1',
)
print(response.status_code)
print(response.json())
