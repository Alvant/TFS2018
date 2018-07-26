#!/bin/python

import psycopg2

try:
	conn = psycopg2.connect(
		host = 'localhost',
		database = 'shop_data',
		user = 'postgres',
		password = 'postgres'
	)
except:
	print 'Failed'
finally:
	if conn is not None:
		conn.close()
		print 'Connection closed'