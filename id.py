import requests

url = "https://api.coingecko.com/api/v3/coins/list"

headers = {
    "accept": "application/json",
    "x-cg-demo-api-key": "CG-52G2YepJGFahyRVfKrxsU1Mf"
}

response = requests.get(url, headers=headers)

# Parse the JSON response
response_date = response.json()

# Create a dictionary to map symbols to IDs
id_mapping = {crypto['symbol']: crypto['name'] for crypto in response_date}

# List of cryptocurrencies you are interested in
cryptocurrencies = ['ethereum', 'solana', 'polkadot', 'polygon-ecosystem-token', 'kusama', 'cosmos', 'dydx-chain', 'near', 'the-open-network', 'tron', 'cardano', 'sei-network', 'sui']

# Initialize an empty dictionary to store the IDs for each cryptocurrency
id_dict = {}

for crypto in cryptocurrencies:
    if crypto in id_mapping:
        id_dict[crypto] = id_mapping[crypto]
    else:
        print(f"No ID found for {crypto}")

print(id_dict)