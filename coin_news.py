import requests

def getNews():
    url = "https://min-api.cryptocompare.com/data/v2/news/?lang=EN"
    response = requests.get(url)
    data = response.json()

    return data['Data']
        