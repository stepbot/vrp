from random import randint,uniform
from math import sqrt,inf
from operator import itemgetter


def OrderGenerator(numOfOrders,quantityLimit,distanceLimit):
    orders = []
    for i in range(numOfOrders):
        order = {}
        order['id']=i
        order['quantity']=randint(1,quantityLimit)
        order['x']=uniform(0,distanceLimit)
        order['y']=uniform(0,distanceLimit)

        orders.append(order)

    return orders




def Distance(x,y):
    distance = sqrt((x*x)+(y*y))
    return distance

def RandomRouter(trucks,orders):
    schedule = {}
    schedule['queues'] = []
    schedule['directCost'] = inf
    schedule['oppurtunityCost'] = inf
    schedule['totalCost'] = inf
    schedule['requiredTime'] = inf

    for truck in trucks:
        queue = {}
        queue['truck'] = truck
        queue['orders'] = []
        queue['directCost'] = inf
        queue['oppurtunityCost'] = inf
        queue['totalCost'] = inf
        queue['requiredTime'] = inf
        schedule['queues'].append(queue)

    for order in orders:
        queue = schedule['queues'][randint(0,len(trucks)-1)]
        queue['orders'].append(order)


    return schedule

def HeuristicRouter(trucks,orders):
    schedule = {}
    schedule['queues'] = []
    schedule['directCost'] = inf
    schedule['oppurtunityCost'] = inf
    schedule['totalCost'] = inf
    schedule['requiredTime'] = inf

    trucks.sort(key=itemgetter('capacity'))
    orders.sort(key=itemgetter('quantity'),reverse=True)

    for truck in trucks:
        queue = {}
        queue['truck'] = truck
        queue['orders'] = []
        queue['directCost'] = inf
        queue['oppurtunityCost'] = inf
        queue['totalCost'] = inf
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
    schedule['directCost'] = 0.0
    schedule['oppurtunityCost'] = 0.0
    schedule['totalCost'] = 0.0
    speed = 45
    for queue in schedule['queues']:
        queue['directCost'] = 0.0
        queue['oppurtunityCost'] = 0.0
        queue['totalCost'] = 0.0
        queue['requiredTime'] = 0.0
        truck = queue['truck']
        for order in queue['orders']:
            if order['quantity'] > truck['capacity']:
                schedule['directCost'] = inf
                queue['directCost'] = inf
                queue['oppurtunityCost'] = inf
                queue['totalCost'] = inf
                queue['requiredTime'] = inf
            else:
                distance = Distance(int(order['x']),int(order['y']))
                marginalTime = ((2*distance)/speed)
                queue['requiredTime'] += marginalTime
                directMarginalCost = marginalTime*int(truck['cost'])
                oppurtunityMarginalCost = directMarginalCost*((truck['capacity']-order['quantity'])/truck['capacity'])
                queue['directCost'] += directMarginalCost
                schedule['directCost']+= directMarginalCost
                queue['oppurtunityCost'] += oppurtunityMarginalCost
                schedule['oppurtunityCost']+= oppurtunityMarginalCost

                queue['totalCost'] += directMarginalCost
                schedule['totalCost']+= directMarginalCost
                queue['totalCost'] += oppurtunityMarginalCost
                schedule['totalCost']+= oppurtunityMarginalCost

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
        if schedule['totalCost'] < bestCost:
            bestSchedule = schedule
            bestCost = schedule['totalCost']

    return bestSchedule

exampleTrucks = [{"id":0,"capacity":5,"cost":60},{"id":1,"capacity":5,"cost":60},{"id":2,"capacity":10,"cost":90}]
exampleOrders = OrderGenerator(20,10,35)
'''
print('using randomOptimizer')
exampleSchedule = RandomOptimizer(exampleTrucks,exampleOrders,1000000)
print(exampleSchedule)
print('schedule passes validation? ', SimpleScheduleValidator(exampleSchedule,exampleOrders))
print('total cost of schedule: $',exampleSchedule['totalCost'])
print('total time of schedule: ',exampleSchedule['requiredTime'],'h')
'''

print('using HeuristicRouter')
exampleSchedule = HeuristicRouter(exampleTrucks,exampleOrders)
exampleSchedule = SimpleScheduleEval(exampleSchedule)
print(exampleSchedule)
print('schedule passes validation? ', SimpleScheduleValidator(exampleSchedule,exampleOrders))
print('total cost of schedule: $',exampleSchedule['totalCost'])
print('total time of schedule: ',exampleSchedule['requiredTime'],'h')
