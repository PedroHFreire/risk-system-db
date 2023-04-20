import unittest
import sqlite3
import os
import sys
import datetime as dt
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts', 'etl'))
import stock_history

class TestPortfolioManagementDatabase(unittest.TestCase):
    def test_stock_history_columns(self):
        conn = sqlite3.connect('stable.db')
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(stock_history)")
        columns = cursor.fetchall()

        expected_columns = [
            ('asset_id', 'INTEGER'),
            ('date', 'DATE'),
            ('open', 'REAL'),
            ('high', 'REAL'),
            ('low', 'REAL'),
            ('close', 'REAL'),
            ('adjusted_close', 'REAL'),
            ('volume', 'INTEGER')
        ]

        self.assertEqual(len(columns), len(expected_columns))

        for i, column in enumerate(columns):
            self.assertEqual(column[1], expected_columns[i][0])
            self.assertEqual(column[2], expected_columns[i][1])

        conn.close()

    def test_download_historical_data(self):
        symbol = 'BBAS3'
        start_date = dt.datetime(2021, 1, 1)
        end_date = dt.datetime(2021, 1, 10)
        historical_data = stock_history.download_historical_data(symbol, stock_history.mt5.TIMEFRAME_D1, start_date, end_date)
        self.assertIsNotNone(historical_data)
        self.assertGreater(len(historical_data.index), 0)

    def test_check_and_update_history(self):
        conn = sqlite3.connect('stable.db')
        cursor = conn.cursor()

        # Get the current row count of stock_history table
        cursor.execute("SELECT COUNT(*) FROM stock_history")
        initial_row_count = cursor.fetchone()[0]

        # Get the first stock from the stocks table
        cursor.execute("SELECT asset_id, ticker FROM stocks LIMIT 1")
        asset_id, ticker = cursor.fetchone()

        # Check and update stock_history
        stock_history.check_and_update_history(asset_id, ticker, cursor)

        # Get the updated row count of stock_history table
        cursor.execute("SELECT COUNT(*) FROM stock_history")
        updated_row_count = cursor.fetchone()[0]

        # Check if the table has been updated with new data
        self.assertGreater(updated_row_count, initial_row_count)

        conn.close()

    def test_update_stock_history(self):
        conn = sqlite3.connect('stable.db')
        cursor = conn.cursor()

        # Get the current row count of stock_history table
        cursor.execute("SELECT COUNT(*) FROM stock_history")
        initial_row_count = cursor.fetchone()[0]

        # Get the first stock from the stocks table
        cursor.execute("SELECT asset_id, ticker FROM stocks LIMIT 1")
        asset_id, ticker = cursor.fetchone()

        # Update stock_history with a new date range
        start_date = dt.datetime(2022, 12, 17)
        end_date = dt.datetime(2022, 12, 31)
        stock_history.update_stock_history(start_date, end_date, asset_id, ticker, cursor)

        # Get the updated row count of stock_history table
        cursor.execute("SELECT COUNT(*) FROM stock_history")
        updated_row_count = cursor.fetchone()[0]

        # Check if the table has been updated with new data
        self.assertGreater(updated_row_count, initial_row_count)

        conn.close()

if __name__ == '__main__':
    unittest.main()
