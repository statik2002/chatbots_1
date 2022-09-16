import os
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()
devman_token = os.environ['DEVMAN_TOKEN']

url = 'https://dvmn.org/api/user_reviews/'

header = {
    'Authorization': f'Token {devman_token}',
}

response = requests.get(url, headers=header)
response.raise_for_status()

pprint(response.json())
