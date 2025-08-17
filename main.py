import time
import requests
from prometheus_client import start_http_server, Gauge

# Create a Gauge metric to track the price of Bitcoin.
# A Gauge is used because the price can go both up and down.
BITCOIN_PRICE_GAUGE = Gauge(
    'bitcoin_price_usd',
    'Current price of Bitcoin in USD.'
)

def fetch_bitcoin_price(url):
    """
    Fetches the current Bitcoin price from a public API.
    
    Args:
        url (str): The API endpoint to fetch the price from.
        
    Returns:
        float: The current Bitcoin price, or None if the request fails.
    """
    try:
        # Make the HTTP GET request to the public API
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            print(f"Successfully received API response. Raw data: {data}")
            # The previous CoinDesk API is now unreliable.
            # This updated code uses the Coinbase API.
            # The price is now at data['data']['amount'] as a string, so we convert it to float.
            price = float(data['data']['amount'])
            return price
        else:
            print(f"Failed to fetch price. Status code: {response.status_code}")
            print(f"Response text: {response.text}") # Print the raw response for debugging
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error parsing JSON response: {e}. Check if API response format has changed.")
        return None

def run_price_collection_loop(url, interval):
    """
    Periodically fetches the Bitcoin price and updates the Prometheus Gauge.
    """
    print(f"Starting Bitcoin price collection loop...")
    while True:
        # Fetch the price and update the gauge
        price = fetch_bitcoin_price(url)
        if price is not None:
            BITCOIN_PRICE_GAUGE.set(price)
            print(f"Updated Bitcoin price metric: {price:.2f} USD")
        else:
            print("Price fetch failed, skipping metric update.")
        
        # Wait for the specified interval before the next update
        time.sleep(interval)

if __name__ == '__main__':
    # Start the Prometheus HTTP server.
    # Metrics will be available at http://localhost:8000
    while True:
        try:
            start_http_server(8000)
            print("Prometheus metrics server started on port 8000.")
            break  # Exit the loop if the server starts successfully
        except OSError as e:
            print(f"Failed to start server on port 8000: {e}. Retrying in 5 seconds...")
            time.sleep(5)
    
    # Define the API endpoint and the collection interval
    api_url = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
    collection_interval = 15  # seconds

    # Run the main application loop.
    run_price_collection_loop(api_url, collection_interval)
