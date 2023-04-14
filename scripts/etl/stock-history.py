import sqlite3
import pandas as pd
from pandas_datareader import data as pdr

def update_stock_history(start_date, end_date):
    # Connect to the database
    conn = sqlite3.connect('stable.db')

    # Create a cursor
    cursor = conn.cursor()

    # Retrieve the list of assets from the stocks table
    cursor.execute('SELECT asset_id, ticker, exchange FROM stocks')
    assets = cursor.fetchall()

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

            # Insert the stock data into the stock_history table
            cursor.execute('INSERT INTO stock_history (asset_id, date, open, high, low, close, adjusted_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (asset_id, date, open_price, high, low, close, adjusted_close, volume))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

# Example usage: update the stock_history table with data from January 1, 2020 to December 31, 2020
update_stock_history('2018-12-31', '2022-12-16')