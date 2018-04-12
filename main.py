from random import randint
from math import sqrt,inf


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

def RandomRouter(trucks,orders):
    schedule = {}
    schedule['queues'] = []
    schedule['cost'] = inf
    for truck in trucks:
        queue = {}
        queue['truck'] = truck
        queue['orders'] = []
        queue['cost'] = inf
        schedule['queues'].append(queue)

    for order in orders:
        queue = schedule['queues'][randint(0,len(trucks)-1)]
        queue['orders'].append(order)


    return schedule


def SimpleScheduleEval(schedule):
    schedule['cost'] = 0.0
    speed = 45
    for queue in schedule['queues']:
        queue['cost'] = 0.0
        truck = queue['truck']
        for order in queue['orders']:
            if order['quantity'] > truck['capacity']:
                schedule['cost'] = inf
                queue['cost'] = inf
            else:
                distance = Distance(int(order['x']),int(order['y']))
                marginalCost = ((2*distance)/speed)*int(truck['cost'])
                queue['cost'] += marginalCost
                schedule['cost']+= marginalCost

    return schedule

def randomOptimizer(trucks,orders,attempts):
    canidateSchedules = []
    bestCost = inf
    bestSchedule = SimpleScheduleEval(RandomRouter(trucks,orders))
    for i in range(attempts):
        canidateSchedules.append(SimpleScheduleEval(RandomRouter(trucks,orders)))

    for schedule in canidateSchedules:
        if schedule['cost'] < bestCost:
            bestSchedule = schedule
            bestCost = schedule['cost']

    return bestSchedule



exampleSchedule = randomOptimizer(exampleTrucks,exampleOrders,1000)
print(exampleSchedule)
print('total cost of schedule: ',exampleSchedule['cost'])
