import requests
import pandas as pd
import datetime

# List of cryptocurrencies
cryptocurrencies = ['ethereum', 'solana', 'polkadot', 'polygon-ecosystem-token', 'kusama', 'cosmos', 'dydx-chain', 'near', 'the-open-network', 'tron', 'cardano', 'sei-network', 'sui']

def get_ath_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/markets/?vs_currency=usd&ids={coin_id}"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-52G2YepJGFahyRVfKrxsU1Mf"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    ath_price = data[0]['ath']
    ath_date = data[0]['ath_date']
    current_price = data[0]['current_price']
    
    return ath_price, ath_date, current_price

for crypto in cryptocurrencies:
    # Fetch 4 years of Bitcoin data from CoinGecko
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days=365"
    # Add headers if the API requires an API key
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-52G2YepJGFahyRVfKrxsU1Mf"
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
    average_price = prices['price'].mean()
    ath_price, ath_date, current_price = get_ath_price(crypto)
    print(f"{crypto} 4YAP: ${average_price:.2f}")
    print(f"{crypto} Current Price: ${current_price}")
    print(f"{crypto} ATH: ${ath_price:.2f}")
    print(f"{crypto} ATH Date: ${ath_date}")