import json
from vrp import OrderGenerator

trucks = [{"id": 0, "capacity": 5, "maxOrdersPerRun": 2, "cost": 60, "homeX":0, "homeY":0, "x":0, "y":0, "homeTime":7, "time":7, "turnAroundTime":0.1667, "unloadTime":0.0833}, {"id": 1, "capacity": 5, "maxOrdersPerRun": 2, "cost": 60, "homeX":0, "homeY":0, "x":0, "y":0, "homeTime":7, "time":7, "turnAroundTime":0.1667, "unloadTime":0.0833}, {"id": 2, "capacity": 10, "maxOrdersPerRun": 2, "cost": 90, "homeX":0, "homeY":0, "x":0, "y":0, "homeTime":7, "time":7, "turnAroundTime":0.25, "unloadTime":0.0833}]

with open('data/trucks.json','w') as outfile:
    json.dump(trucks,outfile)

orders = OrderGenerator(20,10,35)

with open('data/orders.json','w') as outfile:
    json.dump(orders,outfile)
