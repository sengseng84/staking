import requests
import pandas as pd
import time

# List of cryptocurrencies
cryptocurrencies = ['ethereum', 'solana', 'polkadot', 'polygon-ecosystem-token', 'kusama', 'cosmos', 'dydx-chain', 'near', 'the-open-network', 'tron', 'cardano', 'sei-network', 'sui']

# Initialize an empty DataFrame to store all the data
all_prices = pd.DataFrame()

for crypto in cryptocurrencies:
    # Construct the URL with the API key (if required)
    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days=365"
    
    # Add headers if the API requires an API key
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-52G2YepJGFahyRVfKrxsU1Mf"
    }
    
    # Make the GET request
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        prices_data = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
        
        # Convert timestamps to datetime objects
        prices_data['date'] = pd.to_datetime(prices_data['timestamp'], unit='ms')
        
        # Append the data to the main DataFrame
        all_prices = pd.concat([all_prices, prices_data], ignore_index=True)
    else:
        print(f"Failed to retrieve {crypto} data:", response.status_code, response.text)

    # Wait for 1 second between requests
    time.sleep(1)

# Calculate the average price for each cryptocurrency over the past 365 days
for crypto in cryptocurrencies:
    # Filter the data for the specific cryptocurrency
    crypto_prices = all_prices[(all_prices['date'] >= pd.Timestamp.now() - pd.Timedelta(days=365)) & (all_prices['date'].dt.date <= pd.Timestamp.now().date())]
    
    if not crypto_prices.empty:
        average_price = crypto_prices['price'].mean()
        print(f"{crypto} 365-day average price: ${average_price:.2f}")
    else:
        print(f"Insufficient data for {crypto}")
