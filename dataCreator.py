import json
from vrp import OrderGenerator

trucks = [{"id":0,"capacity":5,"maxOrdersPerRun":2,"cost":60},{"id":1,"capacity":5,"maxOrdersPerRun":2,"cost":60},{"id":2,"capacity":10,"maxOrdersPerRun":2,"cost":90}]

with open('trucks.json','w') as outfile:
    json.dump(trucks,outfile)

orders = OrderGenerator(10,10,35)

with open('orders.json','w') as outfile:
    json.dump(orders,outfile)
