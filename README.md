# Telegram to MT5 Forex Signals Copier

## Overview

This project is an advanced forex trading tool that copies signals from Telegram channels directly to MetaTrader 5 (MT5). It features a user-friendly PyQt5-based graphical interface and uses Telegram as both a signal source and an authentication mechanism. The tool appears as a regular user in Telegram channels, allowing for seamless integration and signal copying. With its versatile magic keys, comprehensive account analysis, and advanced features like trailing stop loss, this application provides a complete suite for forex traders.

## Key Features

- **Telegram to MT5 Signal Copying**: Automatically copy forex trading signals from specified Telegram channels to your MetaTrader 5 platform.
- **Telegram-based Authentication**: Use your Telegram account to log in and out of the application securely.
- **User API Integration**: Utilizes Telethon, a Telegram user API, to interact with Telegram as a regular user rather than a bot.
- **MetaTrader 5 Integration**: Directly interfaces with MT5 for executing trades based on received signals.
- **Algorithmic Trading Support**: Compatible with MT5's algorithmic trading features.
- **Versatile Magic Keys**: A comprehensive set of trading tools and shortcuts for efficient trading operations.
- **Account Analysis Pages**: In-depth analysis tools for monitoring and optimizing your trading performance.
- **Trailing Stop Loss**: Advanced risk management feature to protect profits while allowing for potential gains.
- **Data Analysis**: Employs numpy for advanced numerical computations and signal analysis.
- **GUI**: Intuitive PyQt5-based interface for easy configuration and monitoring.
- **Database Management**: Uses SQLite for efficient storage and retrieval of signal and trading data.
- **CSV Handling**: Import and export functionality for signal data in CSV format.

## Advanced Features

### Magic Keys
The Magic Keys feature provides a powerful set of tools for rapid trade execution and management:
- One-click trading for instant market entry
- Quick position sizing based on risk percentage
- Instant close of all positions or specific symbol positions
- Break-even function for open trades
- Quick reversal of positions
- Custom hotkeys for frequently used actions

### Account Analysis
The Account Analysis pages offer comprehensive insights into your trading performance:
- Detailed profit/loss analysis by day, week, and month
- Trade distribution charts
- Win/loss ratios and average trade statistics
- Drawdown analysis
- Performance metrics by currency pair and trading session

### Trailing Stop Loss
The application includes an advanced trailing stop loss feature:
- Automatically adjust stop loss levels as the market moves in your favor
- Customizable trailing distance
- Option to apply trailing stop to individual trades or globally
- Visual representation of trailing stop levels on charts

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7+
- MetaTrader 5 platform installed with algorithmic trading enabled
- Telegram account for authentication and signal reception
- Access to the Telegram channels you wish to copy signals from

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/telegram-mt5-signals-copier.git
   ```

2. Navigate to the project directory:
   ```
   cd telegram-mt5-signals-copier
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your config.py file with your Telegram API credentials:
   ```python
   api_id = "your_api_id"
   api_hash = "your_api_hash"
   ```

## Configuration

1. Ensure your MetaTrader 5 platform is properly set up with algorithmic trading enabled.
2. Obtain your Telegram API credentials (api_id and api_hash) from https://my.telegram.org.
3. Update the `config.py` file with your Telegram API credentials.
4. In the application, you'll need to specify the Telegram channels from which you want to copy signals.

## Usage

To run the application:

```
python main.py
```

1. Upon first run, you'll be prompted to log in with your Telegram account.
2. Configure the Telegram channels you want to monitor for signals.
3. Ensure your MT5 platform is running and properly configured for algorithmic trading.
4. Explore the Magic Keys interface to set up your preferred trading shortcuts.
5. Use the Account Analysis pages to monitor your trading performance.
6. Configure the trailing stop loss feature according to your risk management strategy.
7. The application will now monitor the specified channels and copy signals to your MT5 platform, while providing you with advanced trading tools and analysis.

## Important Notes

- This application uses Telethon, a Telegram user API. This means it will appear as a regular user in Telegram channels, not as a bot.
- Ensure you have the necessary permissions to copy and use signals from the Telegram channels you're monitoring.
- Always practice responsible trading and be aware of the risks involved in forex trading.
- Familiarize yourself with all features, especially the Magic Keys and trailing stop loss, before using them in live trading.

## Algorithmic Trading in MT5

To use this tool effectively:

1. In your MetaTrader 5 platform, ensure that algorithmic trading is enabled.
2. Go to Tools -> Options -> Expert Advisors.
3. Check the box that says "Allow automated trading".
4. You may also need to configure other settings based on your specific trading strategy.

## Contributing

Contributions to this project are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License

This project uses the following license: [License Name].

## Contact

If you want to contact me, you can reach me at `<your_email@example.com>`.

## Disclaimer

This software is for educational and informational purposes only. It is not intended as financial advice or a recommendation to trade. Always understand and comply with the terms of service of any platforms or channels you interact with. The developers are not responsible for any financial losses incurred through the use of this software.

## Acknowledgements

- [MetaTrader 5](https://www.metatrader5.com/)
- [Telethon](https://docs.telethon.dev/en/latest/)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)
