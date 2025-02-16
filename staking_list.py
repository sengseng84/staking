import requests
import os
import pandas as pd
import time
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("COINGECKO_API_KEY")

# Global list to store stakes
stakes = []

def list_stakes():
    """Fetch and display all Proof-of-Stake tokens, storing them in stakes."""
    global stakes  # Ensure we're modifying the global stakes list

    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=proof-of-stake-pos"
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": api_key
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Add index and store data in stakes
        stakes = [{"index": index, **token} for index, token in enumerate(data, start=1)]

        # Print the tokens with index
        print("\n=== List of Proof-of-Stake Tokens ===")
        for token in stakes:
            print(f"{token['index']}. Ticker: {token['symbol'].upper()}, Name: {token['name']}")

    else:
        print("Failed to fetch data:", response.status_code, response.text)

def get_avg(crypto):
    # Initialize an empty DataFrame to store all the data
    all_prices = pd.DataFrame()

    url = f"https://api.coingecko.com/api/v3/coins/{crypto}/market_chart?vs_currency=usd&days=365"
    
    # Add headers if the API requires an API key
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": api_key
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    prices['date'] = pd.to_datetime(prices['timestamp'], unit='ms')
    average_price = prices['price'].mean()
    return average_price

def predict_performance(current_price, ath_price, avg_4y_price, apy, years=3):
    # Metric calculations
    ath_diff_pct = (current_price / ath_price - 1) * 100
    avg_diff_pct = (current_price / avg_4y_price - 1) * 100
    
    # Scenario 1: ATH Recovery
    ath_return = (ath_price / current_price) ** (1/years) - 1
    ath_total = (1 + ath_return) ** years * (1 + apy/100) ** years - 1
    
    # Scenario 2: Mean Reversion
    avg_return = (avg_4y_price / current_price) ** (1/years) - 1
    avg_total = (1 + avg_return) ** years * (1 + apy/100) ** years - 1
    
    # Scenario 3: Sideways
    sideways_total = (1 + apy/100) ** years - 1
    
    # Scenario 4: Bear Case (50% drop)
    bear_return = -0.5
    bear_total = (1 + bear_return) * (1 + apy/100) ** years - 1
    
    return {
        "ATH Recovery (Annualized)": f"{ath_return*100:.1f}%",
        "ATH Recovery + Staking (Total)": f"{ath_total*100:.1f}%",
        "Mean Reversion (Annualized)": f"{avg_return*100:.1f}%",
        "Mean Reversion + Staking (Total)": f"{avg_total*100:.1f}%",
        "Sideways (Staking Only)": f"{sideways_total*100:.1f}%",
        "Bear Case (-50% + Staking)": f"{bear_total*100:.1f}%",
        "Current vs. ATH": f"{ath_diff_pct:.1f}% below ATH",
        "Current vs. 4Y Avg": f"{avg_diff_pct:.1f}% vs. historical average"
    }

def get_stake_by_index():
    """Prompt the user for an index, display details, and predict performance with APY."""
    if not stakes:
        print("No tokens available. Please list tokens first (option 1).")
        return
    
    try:
        index = int(input("\nEnter the token index: "))
        token = next((t for t in stakes if t["index"] == index), None)

        if not token:
            print("Invalid index. Please try again.")
            return

        # Display basic details
        print("\n=== Token Details ===")
        print(f"Index: {token['index']}")
        print(f"Ticker: {token['symbol'].upper()}")
        print(f"Name: {token['name']}")
        print(f"Market Cap: ${token['market_cap']:,.2f}")
        print(f"Current Price: ${token['current_price']:,.2f}")
        
        # Get 4-year average price (updated from original 1-year)
        avg_4y_price = get_avg(token['id'])
        print(f"4-Year Average Price: ${avg_4y_price:,.2f}")
        
        print(f"All-Time High: ${token['ath']:,.2f}")

        # Get APY input
        while True:
            try:
                apy = float(input("\nEnter the staking APY for this token (e.g., 5.5 for 5.5%): "))
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Run prediction
        prediction = predict_performance(
            current_price=token['current_price'],
            ath_price=token['ath'],
            avg_4y_price=avg_4y_price,
            apy=apy,
            years=3  # Default to 3-year prediction
        )

        # Display results
        print("\n=== 3-Year Performance Prediction ===")
        for key, value in prediction.items():
            print(f"{key}: {value}")

    except ValueError:
        print("Invalid input. Please enter a number.")
    except Exception as e:
        print(f"Error: {str(e)}")
        
def main():
    """Interactive menu for the user."""
    while True:
        print("\n=== PoS Token Tracker ===")
        print("1. List all Proof-of-Stake tokens")
        print("2. View token details by index")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            list_stakes()
        elif choice == "2":
            get_stake_by_index()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# Run the interactive menu
main()
