from apps.Emdad.models import Service, Motor
from apps.EmdadUser.models import CustomUser, Technician
from apps.company.models import Expend
from apps.Transaction.models import Transaction
from apps.Order.models import Order
import csv
import os
import django
from datetime import datetime, time


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")
django.setup()

exit()


apss.Order.objects.all().delete()
Transaction.objects.all().delete()
CustomUser.objects.all().delete()
Service.objects.all().delete()
Motor.objects.all().delete()
Technician.objects.all().delete()
Expend.objects.all().delete()


path = 'data/Agents.csv'
file = open(path, 'r')
agentreader = csv.DictReader(file)

User = []
tech = []
for row in agentreader:
    user_data = {'first_name': row['first_name'], 'id': row['id'],
                 'last_name':  row['last_name'],
                 'phone': row['phone1'],
                 'raw_password': 1
                 }
    User.append(user_data)

CustomUser.objects.bulk_create([CustomUser(**data) for data in User])
print("############################\n user inserrted")

for row in agentreader:
    tech_data = {'id': row['id'],
                 'user': CustomUser.objects.get(pk=row['id']),
                 'address': row['address'],
                 'commission': row['weight'],
                 'comment': row['comment'],
                 'time_shift': row['time_shift'],
                 'activation_status': row['activation_status']}
    tech.append(tech_data)
file.close()


Technician.objects.bulk_create([Technician(**data) for data in tech])
print("############################\n technician inserrted")


##
path = 'data/Leads.csv'
file = open(path, 'r')
leadcsvreader = csv.DictReader(file)
leadcsvreader = list(leadcsvreader)

ordermap = {'id': 'id', 'time': 'time', 'problem': 'services', 'customer_full_name': 'customer_full_name', 'motor_model': 'motors',
            'customer_phone': 'customer_phone', 'address': 'address', 'agent_id': 'technician', 'status': 'status', 'total_price_agent': 'wage'}
Orders = []
servicesset = set()
motors_set = set()

for lead in leadcsvreader:
    servicesset.add(lead['problem'])
    motors_set.add(lead['motor_model'])


serviceslist = list(servicesset)
motors_list = list(motors_set)

Service.objects.bulk_create(
    [Service(**{'name': data}) for data in serviceslist])
print("motors  services")

Motor.objects.bulk_create([Motor(**{'brand': data}) for data in motors_list])
print("motors  inserted")

leadcsvreader = csv.DictReader(file)
leadcsvreader = list(leadcsvreader)
for lead in leadcsvreader:
    extracted_data = {ordermap[field]: lead[field]
                      for field in lead.keys() if field in ordermap}
    extracted_data['technician'] = Technician.objects.get(
        pk=lead['agent_id']) if lead['agent_id'] != '' else None
    extracted_data['wage'] = lead['total_price_agent'] if lead['total_price_agent'] != '' else 0
    motors = [Motor.objects.get(brand=extracted_data.pop('motors'))]
    services = [Service.objects.get(name=extracted_data.pop('services'))]
    order = Order(**extracted_data)
    # Orders.append(order)
    order.save()

    datetime_obj = datetime.strptime(lead['time'], '%Y-%m-%d %H:%M:%S.%f')

    order.services.set(services)
    order.motors.set(motors)
    order.time = datetime_obj
    Orders.append(order)
    order.save()


# file.close()
# apss.Order.objects.bulk_create(Orders)
print("len orders", len(Orders))
print("################################\n orders inserted.")

#
path = 'data/Transactions.csv'
file = open(path, 'r')
transactionscsvreader = csv.DictReader(file)

Tranactions = []
for row in transactionscsvreader:
    if row['category'] == 'واریزی توسط تکنسین':
        trans_data = {
            'time': row['time'],
            'amount': row['company_amount'],
            'technician': Technician.objects.get(pk=row['technician_id'])
        }
        tr = Transaction(**trans_data)
        # tr.save()
        tr.time = datetime.strptime(row['time'], '%Y-%m-%d %H:%M:%S.%f')
        tr.save()
        # Tranactions.append(trans_data)

file.close()
print("tranasactions: ", len(Tranactions))

##
path = 'data/Expanses.csv'
file = open(path, 'r')
expansescsvreader = csv.DictReader(file)

Expanses = []
for row in expansescsvreader:
    Expanses.append(row)
file.close()
print("len expenes", len(Expanses))


# apss.Order.objects.bulk_create(Orders)

Transaction.objects.bulk_create([Transaction(**data) for data in Tranactions])
print("transaction inserted.")

Expend.objects.bulk_create([Expend(**data) for data in Expanses])
print("Expanses inserted.")
