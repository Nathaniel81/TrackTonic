import psycopg2

# Database credentials
dbname = 'tracktonik'
user = 'tracktonik_user'
password = 'kxdtwg9aBrNHpUR4aUCdwBjK7W8QyA8n'
host = 'tracktonik.onrender.com'
port = '5432'

# Establish a connection
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Create a cursor
cur = conn.cursor()

# Execute a query
cur.execute('SELECT * FROM your_table')

# Fetch the results
results = cur.fetchall()

# Close the cursor and connection
cur.close()
conn.close()

# Process the results as needed
