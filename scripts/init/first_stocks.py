import csv
import sqlite3
import os

# Connect to the database
conn = sqlite3.connect('stable.db')
cursor = conn.cursor()

# Define the data folder path
data_folder = os.path.join(os.path.dirname(__file__), 'data')

# Iterate over the CSV files
for filename in ['MSFT.csv', 'JNJ.csv', 'XOM.csv']:
    # Construct the full path to the CSV file
    file_path = os.path.join(data_folder, filename)
    
    with open(file_path, 'r') as f:
        # Use the csv module to read the file
        reader = csv.reader(f)
        # Skip the header row
        next(reader)
        # Iterate over the rows in the CSV file
        for row in reader:
            # Insert the row into the table
            cursor.execute('INSERT INTO stock_history (asset_id, date, open, high, low, close, adjusted_close, volume) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', row)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
