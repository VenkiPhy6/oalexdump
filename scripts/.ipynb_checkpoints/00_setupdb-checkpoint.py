import psycopg2
import pandas as pd

# Connect to the PostgreSQL database inside the Docker container
conn = psycopg2.connect(
    host="postgres",  # Docker service name defined in docker-compose.yml
    port="5432", 
    dbname="openalex", # As defined in docker-compose.yml
    user="oalexer", # As defined in docker-compose.yml
    password="alexandria" # As defined in docker-compose.yml
)
# Create a cursor object
cursor = conn.cursor()

# Open the SQL file and read the content
sql_file_path = './openalex-pg-schema.sql'
with open(sql_file_path, 'r') as file:
    sql = file.read()

# Execute the SQL statements from the file
try:
    cursor.execute(sql)
    conn.commit()  # Commit the transaction
    print("SQL file executed successfully!")
except Exception as e:
    print(f"An error occurred: {e}")
    conn.rollback()  # Rollback in case of an error

# Close the cursor and connection
cursor.close()
conn.close()