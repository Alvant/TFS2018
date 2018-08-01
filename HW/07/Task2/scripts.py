from __future__ import print_function

from datetime import date

from peewee import *
from config import config


params = config()

print('Connecting to the PostgreSQL database...')

db = PostgresqlDatabase(
  params['dbname'],
  host=params['host'],
  port=params['port'],
  user=params['user'],
  password=params['password']
)

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
cola = Good(vendor='The Coca-Cola Company', name='Coca-Cola', description='The holiday comes to us')
cola.save()

order = Order(customer=peter, order_dttm=date(2002, 4, 30), status='OK')
order.save()

order_item_thread = OrderItem(order=order, good=red_thread, quantity=100)
order_item_thread.save()
order_item_needle = OrderItem(order=order, good=needle, quantity=2)
order_item_needle.save()

print('Tables created!\n')


print('Query 1: Insert Good in Order\n')

print('Before:')
print('Order ID | Good')
for oi in OrderItem.select():
  print(oi.order.id, oi.good.name)

print()

order_item_cola = OrderItem(order=order, good=cola, quantity=2)
order_item_cola.save()

print('After:')
print('Order ID | Good')
for oi in OrderItem.select():
  print(oi.order.id, oi.good.name)

print()


print('Query 2: Delete Good from Order\n')

print('Before:')
print('Order ID | Good')
for oi in OrderItem.select():
  print(oi.order.id, oi.good.name)

print()

good_to_be_deleted = OrderItem.select().where(
  (OrderItem.order == order) & (OrderItem.good == needle)).get()

good_to_be_deleted.delete_instance()

print('After:')
print('Order ID | Good')
for oi in OrderItem.select():
  print(oi.order.id, oi.good.name)

print()


print('Query 3: Update Quantity of Good in Order\n')

print('Before:')
print('Order ID | Good | Quantity')
for oi in OrderItem.select():
  print(oi.order.id, oi.good.name, oi.quantity)

print()

order_item_to_be_updated = OrderItem.select().where(
  (OrderItem.order == order) & (OrderItem.good == cola)).get()

order_item_to_be_updated.quantity = 5
order_item_to_be_updated.save()

print('After:')
print('Order ID | Good | Quantity')
for oi in OrderItem.select():
  print(oi.order.id, oi.good.name, oi.quantity)

print()


print('Query 4: Extract All Orders\' Info\n')

query = (Customer
  .select(
    Customer,
    Order.id.alias('order_id'),
    OrderItem.quantity.alias('orderitem_quantity'),
    Good.name.alias('good_name'),
    Good.vendor.alias('good_vendor'))
  .join(Order)
  .join(OrderItem)
  .join(Good)
)

print('Order ID', 'First Name', 'Last Name', 'Good', 'Vendor', 'Quantity', sep='\t')

for customer in query.objects():
  print(
    customer.order_id,
    customer.first_nm,
    customer.last_nm,
    customer.good_name,
    customer.good_vendor,
    customer.orderitem_quantity,
    sep='\t'
  )

print()


print('Finished!')
print('Database connection closed')
