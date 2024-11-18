import requests
import os
from dotenv import load_dotenv, dotenv_values
import json

load_dotenv()

api_key = os.getenv("ODDS_KEY")
# print(os.getenv("ODDS_KEY"))

sports_url = 'https://api.the-odds-api.com/v4/sports'
sport = 'americanfootball_ncaaf'
# sport = 'basketball_ncaab'
odds_url = f'{sports_url}/{sport}/odds'

# r = requests.get(f'https://api.the-odds-api.com/v4/sports/?apiKey={api_key}')

# print(r.json())

params = {'apiKey': api_key, 'regions': 'us', 'markets': 'h2h,spreads,totals', 'includeLinks': 'true'}

r = requests.get(odds_url, params)

remaining_requests = r.headers['x-requests-remaining']
print(f'{remaining_requests} requests remaining')

arbitrages = []

for event in r.json():
    markets = params['markets'].split(',')
    best_outcomes = {market:[] for market in markets}
    for bookmaker in event['bookmakers']:
        for market in bookmaker['markets']:
            key = market['key']
            for outcome in market['outcomes']:
                if len(best_outcomes[key]) < 2:
                    best_outcomes[key].append(outcome)
                for i in range(len(best_outcomes[key])):
                    if best_outcomes[key][i]['name'] != outcome['name']:
                        continue
                    if best_outcomes[key][i]['price'] >= outcome['price']:
                        continue
                    outcome['bookmaker'] = bookmaker['title']
                    best_outcomes[key][i] = outcome
    
    possible_arbs = {}

    for market, outcomes in best_outcomes.items():
        if not outcomes:
            continue
        price1 = outcomes[0]['price']
        price2 = outcomes[1]['price']
        stake = 100
        x = price1 + price2
        bet1 = ((x - price1) * 10000 // x) / 100
        # bet2 = ((x - price1) * 10000 // x) / 100
        total = bet1 * price1
        if total > stake:
            outcomes.append({'roi': total - stake})
            possible_arbs[market] = outcomes

    if possible_arbs:
        arbitrages.append(possible_arbs)

json_string = json.dumps(arbitrages, indent=4)
print(json_string)