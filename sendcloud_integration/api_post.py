import requests
import json

SENDCLOUD_API_URL = "https://panel.sendcloud.sc/api/v2/"

response = requests.get(SENDCLOUD_API_URL + "parcels", auth=("db4d7ba1ed80480b83c8f1e759ad2c9e","386677d4d07b401d8c0d244af9c92769",))

print(response.text)

print("Now we post the new data...")

new_data = {
    "parcel": {
            "id": input("ID: "),
            "name": input('Name: '),
            "company_name": "Tas-QR product",
            "address": input('Address: '),
            "postal_code": input('Postal Code: '),
            "house_number": input('Civic Number: '),
            "city": input('City: '),
            "country": input('Country: '),
            "telephone": input('Telephone number: '),
            "email": input('Email address: '),
    }
}

headers = {}
headers['Content-Type'] = 'application/json'

post_response = requests.post(headers=headers,url="https://panel.sendcloud.sc/api/v2/parcels", data=json.dumps(new_data), auth=("db4d7ba1ed80480b83c8f1e759ad2c9e","386677d4d07b401d8c0d244af9c92769",))

if post_response.status_code == 200:
    print("Il nuovo ordine è stato inserito con successo\n")
    print(post_response.text)
    print('\n')
    print(json.loads(post_response.text)['parcel']['id'])
else:
    post_response.raise_for_status()

