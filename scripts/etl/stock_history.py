import os
import pandas as pd
import sqlite3
import datetime as dt
import MetaTrader5 as mt5

def download_historical_data(symbol, timeframe, start_date, end_date):
    mt5_historical_data = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)

    if mt5_historical_data.size == 0:
        return None

    historical_data = pd.DataFrame(mt5_historical_data)
    historical_data.rename(columns={'time': 'date', 'tick_volume': 'volume'}, inplace=True)
    historical_data['date'] = pd.to_datetime(historical_data['date'], unit='s')
    historical_data.drop(columns=['spread', 'real_volume'], inplace=True)

    return historical_data

def update_stock_history(start_date, end_date, asset_id, ticker, cursor):
    available_assets = mt5.symbols_get(group='*' + ticker + '*')

    if ticker in [available_assets[n].name for n in range(len(available_assets))]:
        mt5.symbol_select(ticker, True)
    else:
        print(f'Invalid selected asset ({ticker}). Verify if it is available on the broker synchronized with MetaTrader5.')
        return

    stock_data = download_historical_data(ticker, mt5.TIMEFRAME_D1, start_date, end_date)

    if stock_data is not None:
        for index, row in stock_data.iterrows():
            cursor.execute('''
                INSERT OR IGNORE INTO stock_history (asset_id, date, open, high, low, close, adjusted_close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (asset_id, row['date'].date(), row['open'], row['high'], row['low'], row['close'], row['close'], row['volume']))

def check_and_update_history(asset_id, ticker, cursor):
    cursor.execute('SELECT MAX(date) FROM stock_history WHERE asset_id = ?', (asset_id,))
    max_date = cursor.fetchone()[0]

    if max_date is None:
        start_date = dt.datetime(2006, 12, 31)
        end_date = dt.datetime.now()
    else:
        max_date_dt = dt.datetime.strptime(max_date, '%Y-%m-%d').date()
        start_date = max_date_dt + dt.timedelta(days=1)
        end_date = dt.datetime.now()

    update_stock_history(start_date, end_date, asset_id, ticker, cursor)

if __name__ == '__main__':
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), '..', '..', 'stable.db'))
    cursor = conn.cursor()

    cursor.execute("SELECT asset_id, ticker FROM stocks")
    stocks = cursor.fetchall()

    if not mt5.initialize():
        mt5.shutdown()

    for stock in stocks:
        asset_id, ticker = stock
        check_and_update_history(asset_id, ticker, cursor)

    conn.commit()
    conn.close()
    mt5.shutdown()
