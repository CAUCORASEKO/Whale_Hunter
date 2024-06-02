import requests
import time

# Configuration
BINANCE_API_URL = "https://api.binance.com/api/v3/trades"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "DOTUSDT", "DOGEUSDT", "XRPUSDT"]
THRESHOLD = 1000  # Threshold to detect whale trades in BTC
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"
TELEGRAM_CHAT_ID = "your_telegram_chat_id_here"
CHECK_INTERVAL = 3600  # Time interval between checks in seconds (1 hour)
seen_trades = {symbol: set() for symbol in SYMBOLS}  # Dictionary to store seen trade IDs

def get_binance_trades(symbol):
    """
    Get the latest trades for a given symbol from Binance.

    Parameters:
    symbol (str): The trading pair symbol (e.g., 'BTCUSDT').

    Returns:
    list: A list of trades if the request is successful; an empty list otherwise.
    """
    url = f"{BINANCE_API_URL}?symbol={symbol}&limit=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error getting data for {symbol}: {e}")
        return []

def detect_whale_trades(trades, threshold, seen_ids):
    """
    Detect whale trades from a list of trades.

    Parameters:
    trades (list): A list of trades.
    threshold (float): The minimum trade quantity to be considered a whale trade.
    seen_ids (set): A set of trade IDs that have already been processed.

    Returns:
    list: A list of detected whale trades.
    """
    whale_trades = []
    for trade in trades:
        if float(trade['qty']) >= threshold and trade['id'] not in seen_ids:
            whale_trades.append(trade)
            seen_ids.add(trade['id'])  # Mark the trade ID as seen
    return whale_trades

def send_telegram_message(bot_token, chat_id, message):
    """
    Send a message to a Telegram chat.

    Parameters:
    bot_token (str): The Telegram bot token.
    chat_id (str): The chat ID to send the message to.
    message (str): The message text to send.

    Returns:
    dict: The JSON response from the Telegram API if the request is successful; None otherwise.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error when sending message to Telegram: {e}")
        return None

def format_summary_message(symbol, trades):
    """
    Format a summary message for whale trades of a given symbol.

    Parameters:
    symbol (str): The trading pair symbol.
    trades (list): A list of whale trades.

    Returns:
    str: A formatted summary message.
    """
    total_buy_volume = 0
    total_sell_volume = 0
    total_buy_price = 0
    total_sell_price = 0

    for trade in trades:
        trade_type = "Sell" if trade['isBuyerMaker'] else "Buy"
        amount = float(trade['qty'])
        price = float(trade['price'])

        if trade_type == "Buy":
            total_buy_volume += amount
            total_buy_price += price * amount
        else:
            total_sell_volume += amount
            total_sell_price += price * amount

    avg_buy_price = total_buy_price / total_buy_volume if total_buy_volume > 0 else 0
    avg_sell_price = total_sell_price / total_sell_volume if total_sell_volume > 0 else 0

    message = f"Summary for {symbol}:\n"
    message += f"Total Buy Volume: {total_buy_volume:.2f}\n"
    message += f"Total Sell Volume: {total_sell_volume:.2f}\n"
    message += f"Average Buy Price: {avg_buy_price:.5f}\n"
    message += f"Average Sell Price: {avg_sell_price:.5f}\n"

    return message

def main():
    """
    Main function to continuously check for whale trades and send notifications.
    """
    while True:
        for symbol in SYMBOLS:
            trades = get_binance_trades(symbol)
            whale_trades = detect_whale_trades(trades, THRESHOLD, seen_trades[symbol])
            if whale_trades:
                summary_message = format_summary_message(symbol, whale_trades)
                send_telegram_message(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, summary_message)
        time.sleep(CHECK_INTERVAL)  # Wait for the specified interval before checking again

if __name__ == "__main__":
    main()
