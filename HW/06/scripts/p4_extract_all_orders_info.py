from __future__ import print_function

import sys
import argparse

import psycopg2
from config import config

sql_query = """SELECT first_nm, last_nm, goods.name, quantity
FROM customers
JOIN orders
  ON customers.cust_id = orders.cust_id
JOIN order_items
  ON orders.order_id = order_items.order_id
JOIN goods
  ON order_items.good_id = goods.good_id
"""

def extract_all_orders_info():
    conn = None

    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        print('Connected!' + '\n')
 
        cur = conn.cursor()

        print('SQL query to be executed:')
        print(sql_query)

        cur.execute(sql_query)

        print('Extracted rows:')
        rows = cur.fetchall()
        for row in rows:
          print(row)
        print('')

        # conn.commit()

        # print('Commited!' + '\n')

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')
 
 
if __name__ == '__main__':
    extract_all_orders_info()
