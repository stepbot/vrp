from random import randint
from math import sqrt,inf
from operator import itemgetter


exampleTrucks = [{"id":0,"capacity":5,"cost":60},{"id":1,"capacity":5,"cost":60},{"id":2,"capacity":10,"cost":90},{"id":3,"capacity":20,"cost":120}]
exampleOrders = [{"id":0,"quantity":2,"x":10,"y":10},{"id":1,"quantity":2,"x":10,"y":10},{"id":2,"quantity":2,"x":10,"y":10},{"id":3,"quantity":2,"x":10,"y":10},{"id":4,"quantity":8,"x":10,"y":10}]

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
    schedule['requiredTime'] = inf
    for truck in trucks:
        queue = {}
        queue['truck'] = truck
        queue['orders'] = []
        queue['cost'] = inf
        queue['requiredTime'] = inf
        schedule['queues'].append(queue)

    for order in orders:
        queue = schedule['queues'][randint(0,len(trucks)-1)]
        queue['orders'].append(order)


    return schedule

def HeuristicRouter(trucks,orders):
    schedule = {}
    schedule['queues'] = []
    schedule['cost'] = inf
    schedule['requiredTime'] = inf

    trucks.sort(key=itemgetter('capacity'),reverse=True)
    orders.sort(key=itemgetter('quantity'),reverse=True)

    for truck in trucks:
        queue = {}
        queue['truck'] = truck
        queue['orders'] = []
        queue['cost'] = inf
        queue['requiredTime'] = inf
        schedule['queues'].append(queue)

    for order in orders:
        #print('scheduling order ',order['id'])
        for queue in schedule['queues']:
            #print('checking truck ',queue['truck']['id'])
            truck = queue['truck']
            if order['quantity']<= truck['capacity']:
                #print('truck ',truck['id'], ' has sufficient capacity')
                queueLength = len(queue['orders'])
                targetCapacity = truck['capacity']
                currentTruckID = truck['id']
                betterFlag = False
                for comparisonQueue in schedule['queues']:
                    if truck['id'] != comparisonQueue['truck']['id']:
                        if comparisonQueue['truck']['capacity'] == targetCapacity:
                            if len(comparisonQueue['orders']) < queueLength:
                                #print('deffering assignment of order ',order['id'],' to truck ',truck['id'],' as truck ',comparisonQueue['truck']['id'],' is better suited' )
                                betterFlag = True
                if not betterFlag:
                    #print('assigning order ',order['id'],' to truck  ',truck['id'])
                    queue['orders'].append(order)
                    break


    return schedule




def SimpleScheduleEval(schedule):
    schedule['cost'] = 0.0
    speed = 45
    for queue in schedule['queues']:
        queue['cost'] = 0.0
        queue['requiredTime'] = 0.0
        truck = queue['truck']
        for order in queue['orders']:
            if order['quantity'] > truck['capacity']:
                schedule['cost'] = inf
                queue['cost'] = inf
                queue['requiredTime'] = inf
            else:
                distance = Distance(int(order['x']),int(order['y']))
                marginalTime = ((2*distance)/speed)
                queue['requiredTime'] += marginalTime
                marginalCost = marginalTime*int(truck['cost'])
                queue['cost'] += marginalCost
                schedule['cost']+= marginalCost

    maxTime = 0.0
    for queue in schedule['queues']:
        if queue['requiredTime'] > maxTime:
            maxTime = queue['requiredTime']

    schedule['requiredTime'] =  maxTime

    return schedule

def SimpleScheduleValidator(schedule,orders):
    validFlag = True
    numOfOrders = 0
    for queue in schedule['queues']:
        truck = queue['truck']
        for order in queue['orders']:
            numOfOrders += 1
            if order['quantity'] > truck['capacity']:
                validFlag = False
                break
    if  numOfOrders != len(orders):
        print(numOfOrders,' orders scheduled out of ',len(orders))
        validFlag = False

    return validFlag

def RandomOptimizer(trucks,orders,attempts):
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



print('using randomOptimizer')
exampleSchedule = RandomOptimizer(exampleTrucks,exampleOrders,10000)
print(exampleSchedule)
print('schedule passes validation? ', SimpleScheduleValidator(exampleSchedule,exampleOrders))
print('total cost of schedule: $',exampleSchedule['cost'])
print('total time of schedule: ',exampleSchedule['requiredTime'],'h')

print('using HeuristicRouter')
exampleSchedule = HeuristicRouter(exampleTrucks,exampleOrders)
exampleSchedule = SimpleScheduleEval(exampleSchedule)
print(exampleSchedule)
print('schedule passes validation? ', SimpleScheduleValidator(exampleSchedule,exampleOrders))
print('total cost of schedule: $',exampleSchedule['cost'])
print('total time of schedule: ',exampleSchedule['requiredTime'],'h')
