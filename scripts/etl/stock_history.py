import os
import pandas as pd
import sqlite3
import datetime as dt
import MetaTrader5 as mt5

def download_historical_data(symbol, timeframe, start_date, end_date):
    mt5_historical_data = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)

    historical_data = pd.DataFrame(mt5_historical_data)
    historical_data.rename(columns={'time': 'date', 'tick_volume': 'volume'}, inplace=True)
    historical_data['date'] = pd.to_datetime(historical_data['date'], unit='s')
    historical_data.drop(columns=['spread', 'real_volume'], inplace=True)

    return historical_data

def update_stock_history(start_date, end_date):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', '..', 'stable.db'))
    cursor = conn.cursor()

    cursor.execute("SELECT asset_id, ticker FROM stocks")
    stocks = cursor.fetchall()

    if not mt5.initialize():
        mt5.shutdown()

    for stock in stocks:
        asset_id, ticker = stock
        available_assets = mt5.symbols_get(group='*' + ticker + '*')

        if ticker in [available_assets[n].name for n in range(len(available_assets))]:
            mt5.symbol_select(ticker, True)
        else:
            print(f'Invalid selected asset ({ticker}). Verify if it is available on the broker synchronized with MetaTrader5.')
            continue

        stock_data = download_historical_data(ticker, mt5.TIMEFRAME_D1, start_date, end_date)

        for index, row in stock_data.iterrows():
            cursor.execute('''
                INSERT OR IGNORE INTO stock_history (asset_id, date, open, high, low, close, adjusted_close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (asset_id, row['date'].date(), row['open'], row['high'], row['low'], row['close'], row['close'], row['volume']))

    conn.commit()
    conn.close()
    mt5.shutdown()

# Update stocks already in the database
if __name__ == '__main__':
    end_date = dt.datetime.now()
    start_date = end_date - dt.timedelta(days=30)
    update_stock_history(start_date, end_date)

# Update stocks new to the database