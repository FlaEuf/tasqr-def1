import requests

SENDCLOUD_API_URL = "https://panel.sendcloud.sc/api/v2/"

response = requests.get(SENDCLOUD_API_URL + "parcels", auth=('db4d7ba1ed80480b83c8f1e759ad2c9e','386677d4d07b401d8c0d244af9c92769'))

print(response.status_code)

print(response.text)
