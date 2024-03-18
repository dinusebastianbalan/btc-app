from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import datetime

app = Flask(__name__)

# This list will hold the last 60 price values, one for each 10-second interval in the last 10 minutes
bitcoin_prices = []

def fetch_bitcoin_price():
    try:
        # Replace the URL with the actual API endpoint you intend to use.
        response = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
        data = response.json()
        price = data['USD']

        # Append the current price and timestamp to the bitcoin_prices list
        bitcoin_prices.append((price, datetime.datetime.now()))
        # Keep only the last 60 entries (10 minutes of data)
        if len(bitcoin_prices) > 60:
            bitcoin_prices.pop(0)
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")

def get_average_price():
    if bitcoin_prices:
        return sum(price for price, _ in bitcoin_prices) / len(bitcoin_prices)
    else:
        return 0

@app.route('/current_price')
def current_price():
    if bitcoin_prices:
        return jsonify({'Current BTC Price: USD': bitcoin_prices[-1][0]})
    else:
        return jsonify({'error': 'Price data not available'}), 503

@app.route('/average_price')
def average_price():
    return jsonify({'Average BTC Price over the last 10 minutes: USD': get_average_price()})

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=fetch_bitcoin_price, trigger="interval", seconds=10)
    scheduler.start()

    app.run(debug=True,host='0.0.0.0',port=33133)