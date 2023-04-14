import unittest
import sqlite3
import os
import sys
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
            ('date', 'TEXT'),
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

    def test_stock_history_update(self):
        conn = sqlite3.connect('stable.db')
        cursor = conn.cursor()

        # Get the current row count of stock_history table
        cursor.execute("SELECT COUNT(*) FROM stock_history")
        initial_row_count = cursor.fetchone()[0]

        # Update stock_history with a new date range
        stock_history.update_stock_history('2022-12-17', '2022-12-31')

        # Get the updated row count of stock_history table
        cursor.execute("SELECT COUNT(*) FROM stock_history")
        updated_row_count = cursor.fetchone()[0]

        # Check if the table has been updated with new data
        self.assertGreater(updated_row_count, initial_row_count)

        conn.close()

if __name__ == '__main__':
    unittest.main()
