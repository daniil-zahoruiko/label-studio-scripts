import json
import requests

def load_api_key():
    with open('secrets.txt') as f:
        return json.load(f)['API_KEY']
    
def refresh_token(url, api_key):
    response = requests.post(
        f'{url}api/token/refresh/',
    headers={
        'Content-Type': 'application/json'
    },
    json={
        'refresh': f'{api_key}'
    })

    return response.json()['access']