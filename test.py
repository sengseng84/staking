import requests
import pandas as pd

# List of cryptocurrencies
cryptocurrencies = ['ethereum', 'solana', 'polkadot', 'polygon-ecosystem-token', 'kusama', 'cosmos', 'dydx-chain', 'near', 'the-open-network', 'tron', 'cardano', 'sei-network', 'sui']

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
    print(f"{crypto} 4-year average price: ${average_price:.2f}")

