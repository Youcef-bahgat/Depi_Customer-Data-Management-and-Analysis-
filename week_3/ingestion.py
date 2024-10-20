

import pypyodbc as odbc
import pandas as pd

# Connection settings
DRIVER_NAME = 'ODBC Driver 17 for SQL Server'  # Ensure this matches your installed driver
SERVER_NAME = 'Mervat'
DATABASE_NAME = 'finalTest'

# Connection string
connection_string = f'''
DRIVER={{{DRIVER_NAME}}};
SERVER={SERVER_NAME};
DATABASE={DATABASE_NAME};
Trusted_Connection=yes;
'''

# Connect to the database
conn = odbc.connect(connection_string)
print("Connection successful")

# Create a cursor object
cursor = conn.cursor()

# SQL query to fetch data from the SalesForcastDate table
sql_query = "SELECT * FROM SalesForecastingData;"  # Replace with your actual table name

# Execute the query
cursor.execute(sql_query)

# Fetch the column names from the cursor description
columns = [column[0] for column in cursor.description]

# Fetch all rows from the executed query
rows = cursor.fetchall()

# Create a DataFrame from the fetched data
df = pd.DataFrame(rows, columns=columns)

# Close the cursor and connection
cursor.close()
conn.close()

# Display the DataFrame
print(df)



df.to_csv('forecasting_data.csv', index=False)