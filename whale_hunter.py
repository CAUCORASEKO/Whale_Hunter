import requests
import time

# Configuration
# These are the settings we'll use in our script.
# They are defined as global constants for easy modification and access throughout the code.
BINANCE_API_URL = "https://api.binance.com/api/v3/trades"  # URL for Binance's API to fetch trade data
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOTUSDT", "DOGEUSDT", "XRPUSDT"]  # List of trading pairs to monitor
THRESHOLD = 1000  # Threshold to detect large trades ("whale trades"), measured in the quantity of the cryptocurrency
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"  # Telegram bot token (replace with your actual token)
TELEGRAM_CHAT_ID = "your_telegram_chat_id_here"  # Telegram chat ID to send notifications to
CHECK_INTERVAL = 3600  # Time interval between checks in seconds (1 hour)
seen_trades = {symbol: set() for symbol in SYMBOLS}  # Dictionary to store seen trade IDs for each symbol

# General Notes:
# This script monitors large transactions ("whale trades") on Binance for various trading pairs.
# It uses the Binance API to fetch transaction data and sends notifications via Telegram.
# "Whale trades" are defined as those that exceed a certain quantity threshold (THRESHOLD).

def get_binance_trades(symbol):
    """
    Get the latest trades for a specific trading pair from Binance.

    This function makes a GET request to the Binance API to fetch the 1000 most recent
    transactions for the specified symbol.

    Parameters:
    symbol (str): The trading pair symbol (e.g., 'BTCUSDT').

    Returns:
    list: A list of trades if the request is successful; an empty list otherwise.

    Note: If an error occurs during the request, an error message is printed.
    """
    # Construct the full URL with the symbol and limit of 1000 trades
    url = f"{BINANCE_API_URL}?symbol={symbol}&limit=1000"
    try:
        # Make the GET request to the Binance API
        response = requests.get(url)
        # Check if the response was successful (status code 200)
        response.raise_for_status()
        # Return the response data in JSON format (list of trades)
        return response.json()
    except requests.RequestException as e:
        # If an error occurs, print it and return an empty list
        print(f"Error getting data for {symbol}: {e}")
        return []

def detect_whale_trades(trades, threshold, seen_ids):
    """
    Detect large trades ("whale trades") in a list of transactions.

    A "whale trade" is defined as one whose quantity is equal to or greater than the specified threshold.
    This function also avoids duplicates by keeping track of transaction IDs that have already been processed.

    Parameters:
    trades (list): A list of trades.
    threshold (float): The minimum quantity for a trade to be considered a "whale trade."
    seen_ids (set): A set of transaction IDs that have already been processed.

    Returns:
    list: A list of detected "whale" trades.
    """
    whale_trades = []  # Initialize an empty list to store large trades
    for trade in trades:
        # Convert the trade quantity to a float to compare it with the threshold
        # Check if the quantity is greater than or equal to the threshold
        # and if the trade ID hasn't been seen before
        if float(trade['qty']) >= threshold and trade['id'] not in seen_ids:
            whale_trades.append(trade)  # Add the trade to the list of "whale trades"
            seen_ids.add(trade['id'])  # Mark the trade ID as seen to avoid duplicates
    return whale_trades

def send_telegram_message(bot_token, chat_id, message):
    """
    Send a message to a Telegram chat.

    This function uses the Telegram API to send a message to a specific chat.

    Parameters:
    bot_token (str): The Telegram bot token.
    chat_id (str): The ID of the chat to send the message to.
    message (str): The text of the message to send.

    Returns:
    dict: The JSON response from the Telegram API if the request is successful; None otherwise.

    Note: If an error occurs during sending, an error message is printed.
    """
    # Construct the URL for Telegram's API to send messages
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,  # Specify the chat ID
        "text": message  # Specify the text of the message
    }
    try:
        # Make the POST request to the Telegram API
        response = requests.post(url, data=data)
        response.raise_for_status()  # Check if the response was successful
        return response.json()  # Return the response data in JSON format
    except requests.RequestException as e:
        print(f"Error when sending message to Telegram: {e}")
        return None

def format_summary_message(symbol, trades):
    """
    Format a summary message for the "whale" trades of a given symbol.

    This function calculates and formats a summary of "whale" trades,
    including total buy and sell volumes, and average prices.

    Parameters:
    symbol (str): The trading pair symbol.
    trades (list): A list of "whale" trades.

    Returns:
    str: A formatted summary message.
    """
    # Initialize variables to store total volume and total price
    total_buy_volume = 0
    total_sell_volume = 0
    total_buy_price = 0
    total_sell_price = 0

    for trade in trades:
        # Determine if the trade is a buy or a sell
        trade_type = "Sell" if trade['isBuyerMaker'] else "Buy"
        amount = float(trade['qty'])  # Convert the quantity to float
        price = float(trade['price'])  # Convert the price to float

        # Accumulate totals for buys and sells
        if trade_type == "Buy":
            total_buy_volume += amount
            total_buy_price += price * amount  # Multiply by quantity to get the total
        else:
            total_sell_volume += amount
            total_sell_price += price * amount  # Multiply by quantity to get the total

    # Calculate the average prices
    avg_buy_price = total_buy_price / total_buy_volume if total_buy_volume > 0 else 0
    avg_sell_price = total_sell_price / total_sell_volume if total_sell_volume > 0 else 0

    # Format the summary message
    message = f"Summary for {symbol}:\n"
    message += f"Total Buy Volume: {total_buy_volume:.2f}\n"
    message += f"Total Sell Volume: {total_sell_volume:.2f}\n"
    message += f"Average Buy Price: {avg_buy_price:.5f}\n"
    message += f"Average Sell Price: {avg_sell_price:.5f}\n"

    return message

def main():
    """
    Main function to continuously check for "whale" trades and send notifications.

    This function runs in an infinite loop, periodically checking for "whale" trades
    for each symbol in the SYMBOLS list. If "whale" trades are detected,
    a summary message is sent via Telegram.
    """
    while True:
        for symbol in SYMBOLS:
            # Get the latest trades for the symbol
            trades = get_binance_trades(symbol)
            # Detect the "whale" trades
            whale_trades = detect_whale_trades(trades, THRESHOLD, seen_trades[symbol])
            if whale_trades:
                # If "whale" trades were detected, format and send a message
                summary_message = format_summary_message(symbol, whale_trades)
                send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, summary_message)
        # Wait for the specified interval before checking again
        time.sleep(CHECK_INTERVAL)

# Script entry point
# The following line allows the script to run only if invoked directly,
# which is useful to prevent it from running if the file is imported as a module in another script.
if __name__ == "__main__":
    main()
