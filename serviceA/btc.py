import requests
import time

# Placeholder for the actual API URL and API key
API_URL = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD"

def fetch_btc_price():
    """Fetches the current BTC price in USD."""
    response = requests.get(API_URL)
    data = response.json()
    # Assuming the API returns a JSON object with the price in a field named 'price_usd'
    return data['USD']

def calculate_average_price(duration_in_minutes=10, interval_in_seconds=10):
    """Calculates the average BTC price over the last 'duration_in_minutes' minutes."""
    prices = []
    for _ in range(int(duration_in_minutes * 60 / interval_in_seconds)):
        try:
            price = fetch_btc_price()
            print(f"Current BTC Price: USD {price}")
            prices.append(price)
            time.sleep(interval_in_seconds)
        except Exception as e:
            print(f"Error fetching BTC price: {e}")
    return sum(prices) / len(prices) if prices else None

# Example usage
if __name__ == "__main__":
    average_price = calculate_average_price()
    print(f"Average BTC Price over the last 10 minutes: USD {average_price}")
