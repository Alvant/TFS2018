from __future__ import print_function

import sys
import argparse

import psycopg2
from config import config

sql_query = """UPDATE order_items
SET quantity = %s
WHERE
  order_id = %s AND
  good_id = (SELECT good_id FROM goods WHERE goods.name = %s)
"""

def parse_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    'good_name',
    action='store',
    type=str,
    help='name of some good which quantity is to be modified'
  )

  parser.add_argument(
    'order_id',
    action='store',
    type=int,
    help='id of an order where to modify the quantity of good'
  )

  parser.add_argument(
    'quantity',
    action='store',
    type=str,
    help='quantity of good'
  )

  return parser.parse_args()


def update_quantity_of_good_in_order(good_name, order_id, quantity):
    sql_query_args = (quantity, order_id, good_name)
    conn = None

    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        print('Connected!' + '\n')
 
        cur = conn.cursor()

        print("Trying to find the good's id...")
        cur.execute('SELECT good_id FROM goods WHERE goods.name = %s', (good_name,))
        good_id = cur.fetchone()[0]
        print('Done!')
        print('Good "' + good_name + '"\'s' + ' id is ' + str(good_id) + '\n')

        print('SQL query to be executed:')
        print(sql_query % sql_query_args)

        cur.execute(sql_query, sql_query_args)
        conn.commit()

        print('Commited!' + '\n')

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed')
 
 
if __name__ == '__main__':
    args = parse_args()

    print('Arguments got:', args)

    update_quantity_of_good_in_order(
      good_name=args.good_name,
      order_id=args.order_id,
      quantity=args.quantity
    )
