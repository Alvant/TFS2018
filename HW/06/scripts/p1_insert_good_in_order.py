from __future__ import print_function

import sys
import argparse

import psycopg2
from config import config

sql_query = """INSERT INTO order_items
VALUES (
  DEFAULT,
  %s,
  (SELECT good_id FROM goods WHERE goods.name = %s),
  1
)
"""

def parse_args():
  parser = argparse.ArgumentParser()

  parser.add_argument(
    'good_name',
    action='store',
    type=str,
    help='name of some good to add in order'
  )

  parser.add_argument(
    'order_id',
    action='store',
    type=int,
    help='id of an order to add the good into'
  )

  return parser.parse_args()


def insert_good_in_order(good_name, order_id):
    sql_query_args = (order_id, good_name)
    conn = None

    try:
        params = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        print('Connected!')
 
        cur = conn.cursor()

        print('SQL query to be executed:', sql_query % sql_query_args)

        cur.execute(sql, sql_query_args)
        # conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
 
if __name__ == '__main__':
    args = parse_args()

    print('Arguments got:', args)

    insert_good_in_order(
      good_name=args.good_name,
      order_id=args.order_id
    )
