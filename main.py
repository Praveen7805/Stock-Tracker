import requests
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

#getting stock data from alphavantageAPI

# def get_stock_data(symbol, api_key):
#     url = f"https://www.alphavantage.co/query"
#     params = {
#         "function": "TIME_SERIES_INTRADAY",
#         "symbol": symbol,
#         "interval": "5min",
#         "apikey": api_key
#     }
#     response = requests.get(url, params=params)
#     data = response.json()
#     return data.get("Time Series (5min)", {})


def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    return stock.history(period="1d", interval="5m")


#Plotting the received stock data

def plot_stock_data(data, symbol):
    times = list(data.keys())
    prices = [float(data[time]["4. close"]) for time in times]

    plt.figure(figsize=(10, 5))
    plt.plot(times, prices, label=f"{symbol} Price")
    plt.xticks(rotation=45)
    plt.xlabel("Time")
    plt.ylabel("Price (USD)")
    plt.title(f"{symbol} Stock Price")
    plt.legend()
    plt.show()


#exporting the data into a csv file

def save_to_csv(data, symbol):
    file_name = f"{symbol}_stock_data.csv"
    data.to_csv(file_name)
    print(f"Data for {symbol} saved to {file_name}")

#main function

def main():
    api_key = "GQBGT5DEPFKDP0UF"
    symbols = ["AAPL", "GOOGL", "TSLA"]  # Add the stocks you want to track

    for symbol in symbols:
        print(f"Fetching data for {symbol}...")
        #data = get_stock_data(symbol, api_key)  # For Alpha Vantage
        data = get_stock_data(symbol)  # For Yahoo Finance
        print(data)
        # if not data:
        #     print(f"No data found for {symbol}")
        #     continue

        save_to_csv(data, symbol)
        # plot_stock_data(data, symbol)  # Use Matplotlib
        # plot_interactive_chart(data, symbol)  # Use Plotly

if __name__ == "__main__":
    main()
