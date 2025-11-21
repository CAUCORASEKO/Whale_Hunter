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

- **BINANCE_API_URL**: The base URL for the Binance API.  
- **SYMBOLS**: A list of cryptocurrency pairs to monitor (e.g., BTCUSDT, ETHUSDT).  
- **THRESHOLD**: The minimum trade quantity to consider as a whale trade.  
- **TELEGRAM_BOT_TOKEN**: The token for the Telegram bot used to send messages.  
- **TELEGRAM_CHAT_ID**: The chat ID where notifications will be sent.  
- **CHECK_INTERVAL**: The time interval (in seconds) between checks.

## Setup

### Prerequisites

- Python 3.x  
- Required Python packages: `requests`

### Installation

1. Clone the repository:  
   git clone https://github.com/yourusername/whale-hunter.git  
   cd whale-hunter  

2. Install dependencies:  
   pip install requests  

3. Update configuration values in the script:
   - Replace `your_telegram_bot_token_here` with your actual Telegram bot token.
   - Replace `your_telegram_chat_id_here` with your actual Telegram chat ID.

## Usage

To run the script:

python whale_hunter.py

The script will start monitoring the specified cryptocurrency pairs for whale trades and send notifications to the configured Telegram chat.

## Functions

### get_binance_trades(symbol)

Fetches the latest trades for a given symbol from Binance.  
Parameters: `symbol` (str).  
Returns: A list of trades if the request is successful; an empty list otherwise.

### detect_whale_trades(trades, threshold, seen_ids)

Detects whale trades from a list of trades.  
Parameters:  
- `trades` (list): A list of trades  
- `threshold` (float): Minimum trade quantity to consider a whale trade  
- `seen_ids` (set): Trade IDs already processed  
Returns: A list of detected whale trades.

### send_telegram_message(bot_token, chat_id, message)

Sends a message to a Telegram chat.  
Parameters:  
- `bot_token` (str)  
- `chat_id` (str)  
- `message` (str)  
Returns: JSON response from Telegram API or None.

### format_summary_message(symbol, trades)

Creates a formatted summary for whale trades.  
Parameters:  
- `symbol` (str)  
- `trades` (list)  
Returns: Summary message.

### main()

Main function to continuously check for whale trades and send notifications.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Binance API for trade data  
- Telegram Bot API for messaging
