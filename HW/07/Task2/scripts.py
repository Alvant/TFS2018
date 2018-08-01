from __future__ import print_function

from datetime import date

from peewee import *
from config import config


print('Connecting to the PostgreSQL database...')

db = PostgresqlDatabase(**params)

print('Connected!' + '\n')


class Customer(Model):
  first_nm = CharField()
  last_nm = CharField()

  class Meta:
    database = db


class Order(Model):
  customer = ForeignKeyField(Customer)
  order_dttm = DateField()
  status = CharField()

  class Meta:
    database = db


class Good(Model):
  vendor = CharField()
  name = CharField()
  description = CharField()

  class Meta:
    database = db


class OrderItem(Model):
  order = ForeignKeyField(Order)
  good = ForeignKeyField(Good)
  quantity = IntegerField()

  class Meta:
    database = db


Customer.create_table()
Order.create_table()
Good.create_table()
OrderItem.create_table()

jane = Customer(first_nm='Mary', last_nm='Jane')
jane.save()
peter = Customer(first_nm='Peter', last_nm='Parker')
peter.save()

red_thread = Good(vendor='Good Threads Ltd.', name='Red thread', description='High quality')
red_thread.save()
needle = Good(vendor='Good Threads Ltd.', name='Needle', description='Stainless steel')
needle.save()

order = Order(customer=peter, date=date(2002, 4, 30), status='OK')
order.save()

order_item_thread = OrderItem(order=order, good=red_thread, quantity=100)
order_item_thread.save()
order_item_needle = OrderItem(order=order, good=needle, quantity=2)
order_item_needle.save()


print('Finished!')
print('Database connection closed')
