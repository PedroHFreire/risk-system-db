import sqlite3

# Connect to the database
conn = sqlite3.connect("stable.db")
cursor = conn.cursor()

# Get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Loop through the list of tables and drop each one
for table in tables:
    cursor.execute("DROP TABLE {};".format(table[0]))

# Commit the changes and close the connection
conn.commit()
conn.close()