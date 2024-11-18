import requests
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

api_key = os.getenv("ODDS_KEY")
# print(os.getenv("ODDS_KEY"))

sports_url = 'https://api.the-odds-api.com/v4/sports'
sport = 'basketball_ncaab'
odds_url = '{sports_url}/{sport}/odds'

# r = requests.get(f'https://api.the-odds-api.com/v4/sports/?apiKey={api_key}')

# print(r.json())

params = {'apiKey': api_key, 'regions': 'us', 'markets': 'h2h,spreads,totals', 'includeLinks': 'true'}

r = requests.get(odds_url, params)

