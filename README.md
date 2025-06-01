# TradingView MCP Server

A Model Context Protocol (MCP) server that provides real-time stock data and recommendations from TradingView. This server enables AI assistants and other MCP-compatible applications to access comprehensive stock market data including technical indicators, candlestick patterns, and trading recommendations.

## Features

- **Real-time Stock Data**: Fetch current stock prices, volumes, and market capitalizations
- **Technical Analysis**: Access 20+ technical indicators including SMA, EMA, RSI, MACD, Bollinger Bands, and ATR
- **Trading Recommendations**: Get AI-powered buy/sell/hold recommendations based on technical analysis
- **Candlestick Patterns**: Detect 20+ candlestick patterns for enhanced trading signals
- **Indian Market Focus**: Optimized for NSE (National Stock Exchange) stocks including NIFTY and NIFTY Jr indices
- **Data Caching**: Intelligent caching system to reduce API calls and improve performance

## Available Tools

### `get_stock_recommendations()`
Retrieve comprehensive stock recommendations with technical analysis ratings.

**Returns**: A formatted string containing stock recommendations based on multiple technical indicators.

### `check_stock_values(tickers: list[str])`
Get detailed stock information for specific ticker symbols.

**Parameters**:
- `tickers` (list[str]): List of stock ticker symbols to look up

**Returns**: Dictionary containing filtered stock data for the specified tickers.

## Data Fields

The server provides access to 90+ data fields including:

### Basic Information
- Stock name, description, and exchange
- Current price, open, high, low, close
- Volume and relative volume metrics
- Market capitalization

### Technical Indicators
- **Moving Averages**: SMA20, SMA50, SMA100, EMA20, EMA50, EMA200
- **Momentum**: RSI, MACD (signal and histogram)
- **Volatility**: Bollinger Bands (upper, basis, lower), ATR
- **Pivot Points**: Monthly classic resistance and support levels

### Fundamental Data
- Price-to-earnings ratio (P/E TTM)
- Earnings per share (EPS)
- Dividend yield
- Beta (1-year)
- Sector classification

### Candlestick Patterns
Detects 20+ patterns including:
- Doji variations (Standard, Dragonfly, Gravestone)
- Engulfing patterns (Bullish/Bearish)
- Star patterns (Morning/Evening)
- Hammer and Hanging Man
- Marubozu patterns
- And many more...

## Configuration

### Market Settings
Currently configured for the Indian market with focus on:
- NSE (National Stock Exchange)
- NIFTY index components
- NIFTY Jr index components

### API Settings
The server uses TradingView's public scanner API with appropriate headers and rate limiting.

## Error Handling

The server includes comprehensive error handling with custom `TradingviewError` exceptions for:
- API connection failures
- Data parsing errors
- File I/O issues
- Invalid ticker symbols

## Development

### Project Structure
```
TradingviewMCPServer/
├── src/
│   └── mcp_server/
│       ├── __init__.py
│       ├── main.py              # Main MCP server implementation
│       └── constant_variables.py # API configuration and data fields
├── tests/
│   └── __init__.py
├── pyproject.toml              # Project dependencies and metadata
├── poetry.lock                 # Locked dependency versions
├── Dockerfile                  # Container configuration
└── README.md                   # This file
```

### Code Style

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- Type hints throughout the codebase

Format code before committing:
```bash
poetry run black src/
poetry run isort src/
```

## Disclaimer

This tool is for educational and informational purposes only. The stock recommendations and data provided should not be considered as financial advice. Always consult with a qualified financial advisor before making investment decisions.