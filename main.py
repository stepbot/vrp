from random import randint
from math import sqrt

exampleTrucks = [{"id":"0","capacity":"5","cost":"60"},{"id":"1","capacity":"5","cost":"60"},{"id":"2","capacity":"10","cost":"90"}]
exampleOrders = [{"id":"0","quantity":"5","x":"10","y":"10"},{"id":"1","quantity":"5","x":"10","y":"10"},{"id":"2","quantity":"10","x":"10","y":"10"}]

def Distance(x,y):
    distance = sqrt((x*x)+(y*y))
    return distance

def RandomRouter(trucks,orders):
    schedule = {}
    for order in orders:
        schedule[order['id']] = str(randint(0,len(trucks)-1))
    return schedule

def SimpleScheduleEval(trucks,orders,schedule):
    cost = 0
    speed = 45
    for truck in trucks:
        print('truck number ',truck['id'])
        for orderHandle in schedule:
            if schedule[orderHandle] == truck['id']:
                order = orders[int(orderHandle)]
                distance = Distance(int(order['x']),int(order['y']))
                cost += ((2*distance)/speed)*int(truck['cost'])
    return cost


exampleSchedule = RandomRouter(exampleTrucks,exampleOrders)
print(exampleSchedule)
print(SimpleScheduleEval(exampleTrucks,exampleOrders,exampleSchedule))
