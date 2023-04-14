import sqlite3
import pandas as pd
from pandas_datareader import data as pdr

def retrieve_stock_history(start_date, end_date):
    # Connect to the database
    conn = sqlite3.connect('stable.db')

    # Create a cursor
    cursor = conn.cursor()

    # Retrieve the list of assets from the stocks table
    cursor.execute('SELECT asset_id, ticker, exchange FROM stocks')
    assets = cursor.fetchall()

    # Initialize an empty list to store the data
    data = []

    # Iterate through the assets
    for asset in assets:
        asset_id, ticker, exchange = asset

        # Use pandas_datareader to retrieve the stock data from Yahoo Finance
        stock_data = pdr.get_data_yahoo(ticker, start_date, end_date)

        # Iterate through the rows in the stock data DataFrame
        for index, row in stock_data.iterrows():
            date = index.strftime('%Y-%m-%d')
            open_price = row['Open']
            high = row['High']
            low = row['Low']
            close = row['Close']
            adjusted_close = row['Adj Close']
            volume = row['Volume']

            # Add the data to the list
            data.append((asset_id, date, open_price, high, low, close, adjusted_close, volume))

    # Create a DataFrame from the list of data
    df = pd.DataFrame(data, columns=['stock_id', 'date', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume'])

    # Close the connection
    conn.close()

    return df

# Example usage: retrieve stock history data from January 1, 2020 to December 31, 2020
df = retrieve_stock_history('2018-12-31', '2022-12-16')
print(df)