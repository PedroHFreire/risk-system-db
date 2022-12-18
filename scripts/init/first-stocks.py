import csv
import sqlite3

# Connect to the database
conn = sqlite3.connect('stable.db')
cursor = conn.cursor()

# Iterate over the CSV files
for filename in ['MSFT.csv', 'JNJ.csv', 'XOM.csv']:
    with open(filename, 'r') as f:
        # Use the csv module to read the file
        reader = csv.reader(f)
        # Skip the header row
        next(reader)
        # Iterate over the rows in the CSV file
        for row in reader:
            # Insert the row into the table
            cursor.execute('INSERT INTO stock_history (stock_id, date, open, high, low, close, adjusted_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', row)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
