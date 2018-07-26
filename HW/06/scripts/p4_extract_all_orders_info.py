from __future__ import print_function

import pandas as pd

import psycopg2
from config import config

info_file = './outputs/orders_info.csv'

columns_names_to_write_in_file = ['Order No.', 'First Name', 'Last Name', 'Product', 'Vendor', 'Quantity']

sql_query = """SELECT orders.order_id, first_nm, last_nm, goods.name, vendor, quantity
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
        rows = cur.fetchall()
        df = pd.DataFrame(columns=columns_names_to_write_in_file)

        print('Extracted rows:')

        for idx, row in enumerate(rows):
          print(row)
          df.loc[idx] = row

        print('')

        df.to_csv(info_file, index=False, encoding='utf8')

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
