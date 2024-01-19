import psycopg2
import random
import environ

# Initialize environment variables
env = environ.Env()
environ.Env.read_env()

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    user='postgres',
    password=env('DBPASS'),
    database=env('DATABASE')
)

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create tables
print("Creating tables...")

# Products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL NOT NULL,
    stock_quantity INTEGER NOT NULL
)
''')

# Customers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
)
''')

# Orders table - updated to include price
cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    order_price DECIMAL NOT NULL,
    order_date DATE NOT NULL
)
''')

# Insert sample data into products
print("Inserting sample products...")
product_names = ['Product {}'.format(i) for i in range(1, 11)]
for name in product_names:
    price = random.uniform(10, 100)
    cursor.execute("INSERT INTO products (name, price, stock_quantity) VALUES (%s, %s, %s)",
                   (name, price, random.randint(10, 50)))

# Insert sample data into customers
print("Inserting sample customers...")
customer_names = ['Customer {}'.format(i) for i in range(1, 41)]
for name in customer_names:
    email = '{}@example.com'.format(name.replace(' ', '').lower())
    cursor.execute("INSERT INTO customers (name, email) VALUES (%s, %s)",
                   (name, email))

# Generate random orders
print("Generating random orders...")
cursor.execute("SELECT id FROM customers")
customer_ids = [row[0] for row in cursor.fetchall()]
cursor.execute("SELECT id, price FROM products")
products = cursor.fetchall()

for customer_id in customer_ids:
    for _ in range(random.randint(1, 5)):  # Each customer makes 1 to 5 orders
        product_id, price = random.choice(products)
        quantity = random.randint(1, 3)
        order_price = price * quantity
        order_date = '2023-' + str(random.randint(1, 12)).zfill(2) + '-' + str(random.randint(1, 28)).zfill(2)
        cursor.execute("INSERT INTO orders (customer_id, product_id, quantity, order_price, order_date) VALUES (%s, %s, %s, %s, %s)",
                       (customer_id, product_id, quantity, order_price, order_date))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data generation complete.")
