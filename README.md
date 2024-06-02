# Whale Hunter

A Python script to monitor significant (whale) trades on Binance for specific cryptocurrency pairs and send notifications to a Telegram chat.

## Description

This script fetches the latest trade data from the Binance API for a list of specified cryptocurrency pairs. It detects large trades (whale trades) that exceed a predefined threshold and sends a summary of these trades to a Telegram chat. The script runs continuously, checking for new trades at regular intervals.

## Features

- Monitors specified cryptocurrency pairs on Binance.
- Detects whale trades based on a configurable threshold.
- Sends notifications to a Telegram chat with details of detected trades.
- Runs continuously with configurable check intervals.

## Configuration

The script uses several configuration parameters:

- `BINANCE_API_URL`: The base URL for the Binance API.
- `SYMBOLS`: A list of cryptocurrency pairs to monitor (e.g., `BTCUSDT`, `ETHUSDT`).
- `THRESHOLD`: The minimum trade quantity to consider as a whale trade.
- `TELEGRAM_BOT_TOKEN`: The token for the Telegram bot used to send messages.
- `TELEGRAM_CHAT_ID`: The chat ID where notifications will be sent.
- `CHECK_INTERVAL`: The time interval (in seconds) between checks.

## Setup

### Prerequisites

- Python 3.x
- Required Python packages: `requests`

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/whale-hunter.git
    cd whale-hunter
    ```

2. Install the required Python packages:
    ```sh
    pip install requests
    ```

3. Update the configuration values in the script:
    - Replace `your_telegram_bot_token_here` with your actual Telegram bot token.
    - Replace `your_telegram_chat_id_here` with your actual Telegram chat ID.

## Usage

Run the script:
```sh
python whale_hunter.py
The script will start monitoring the specified cryptocurrency pairs for whale trades and send notifications to the configured Telegram chat.
Functions
get_binance_trades(symbol)

Fetches the latest trades for a given symbol from Binance.

    Parameters: symbol (str): The trading pair symbol (e.g., BTCUSDT).
    Returns: A list of trades if the request is successful; an empty list otherwise.

detect_whale_trades(trades, threshold, seen_ids)

Detects whale trades from a list of trades.

    Parameters:
        trades (list): A list of trades.
        threshold (float): The minimum trade quantity to be considered a whale trade.
        seen_ids (set): A set of trade IDs that have already been processed.
    Returns: A list of detected whale trades.

send_telegram_message(bot_token, chat_id, message)

Sends a message to a Telegram chat.

    Parameters:
        bot_token (str): The Telegram bot token.
        chat_id (str): The chat ID to send the message to.
        message (str): The message text to send.
    Returns: The JSON response from the Telegram API if the request is successful; None otherwise.

format_summary_message(symbol, trades)

Formats a summary message for whale trades of a given symbol.

    Parameters:
        symbol (str): The trading pair symbol.
        trades (list): A list of whale trades.
    Returns: A formatted summary message.

main()

Main function to continuously check for whale trades and send notifications.
License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    Binance API for providing trade data.
    Telegram Bot API for sending notifications.

