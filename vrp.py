from random import randint,uniform,shuffle,choice
from math import sqrt,inf
from operator import itemgetter
from collections import deque


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

def DistanceBetween(x1,y1,x2,y2):
    distance = sqrt(((x2-x1)**2)+((y2-y1)**2))
    return distance

def CapacityCheck(run,checkOrder):
    validFlag = True
    quantityTotal = checkOrder['quantity']
    quantityTotal += run['quantity']

    totalOrders = len(run['orders'])+1

    if run['truck']['capacity'] < quantityTotal:
        validFlag = False

    if run['truck']['maxOrdersPerRun'] < totalOrders:
        validFlag = False

    return validFlag

def PrettyPrintSchedule(schedule):
    for queue in schedule['queues']:
        print('Truck ',queue['truck']['id'],' with capacity of ',queue['truck']['capacity'])
        if len(queue['runs']) == 0:
            print('Not used')
        else:
            for ii in range(len(queue['runs'])):
                print('\tRun ',ii,' total of ',queue['runs'][ii]['quantity'],' units')
                for order in queue['runs'][ii]['orders']:
                    print('\t\tOrder ',order['id'],' of ',order['quantity'],' units')






def RandomRouter(trucks,orders):
    schedule = {}
    schedule['queues'] = []
    schedule['directCost'] = inf
    schedule['oppurtunityCost'] = inf
    schedule['totalCost'] = inf
    schedule['requiredTime'] = inf

    runs = []
    shuffle(orders)
    workingOrders = deque(orders)


    workingRun = {}
    workingRun['truck'] = {}
    workingRun['quantity'] = 0
    workingRun['orders'] = deque()

    while len(workingOrders)>0:
        for ii in range(len(workingOrders)):
            if len(workingRun['truck'])==0:
                workingRun['truck'] = choice(trucks)
                workingOrder = workingOrders.pop()
                if CapacityCheck(workingRun,workingOrder):
                    workingRun['orders'].append(workingOrder)
                    workingRun['quantity'] += workingOrder['quantity']
                else:
                    workingOrders.appendleft(workingOrder)
            else:
                workingOrder = workingOrders.pop()
                if CapacityCheck(workingRun,workingOrder):
                    workingRun['orders'].append(workingOrder)
                    workingRun['quantity'] += workingOrder['quantity']
                else:
                    workingOrders.appendleft(workingOrder)
        runs.append(workingRun)
        workingRun = {}
        workingRun['truck'] = {}
        workingRun['quantity'] = 0
        workingRun['orders'] = deque()

    for truck in trucks:
        queue = {}
        queue['truck'] = truck
        queue['runs'] = deque()
        queue['directCost'] = inf
        queue['oppurtunityCost'] = inf
        queue['totalCost'] = inf
        queue['requiredTime'] = inf
        schedule['queues'].append(queue)

    shuffle(runs)

    for queue in schedule['queues']:
        for run in runs:
            if run['truck']['id'] ==  queue['truck']['id']:
                if run['quantity'] > 0:
                    queue['runs'].append(run)

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
    schedule['overheadCost'] = 0.0
    schedule['totalCost'] = 0.0
    speed = 45
    overheadCost = 270

    for queue in schedule['queues']:
        queue['directCost'] = 0.0
        queue['oppurtunityCost'] = 0.0
        queue['totalCost'] = 0.0
        queue['requiredTime'] = 0.0
        truck = queue['truck']
        for run in queue['runs']:
            if run['quantity'] > truck['capacity']:
                schedule['directCost'] = inf
                queue['directCost'] = inf
                queue['oppurtunityCost'] = inf
                queue['totalCost'] = inf
                queue['requiredTime'] = inf
            else:
                truckXPosition = 0
                truckYPosition = 0
                distance = 0

                for order in run['orders']:
                    distance += DistanceBetween(truckXPosition,truckYPosition,order['x'],order['y'])
                    truckXPosition = order['x']
                    truckXPosition = order['y']
                distance += DistanceBetween(truckXPosition,truckYPosition,0,0)

                marginalTime = ((2*distance)/speed)
                queue['requiredTime'] += marginalTime
                directMarginalCost = marginalTime*int(truck['cost'])
                oppurtunityMarginalCost = directMarginalCost*((truck['capacity']-run['quantity'])/truck['capacity'])

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
    schedule['overheadCost'] = schedule['requiredTime']*overheadCost
    schedule['totalCost'] += schedule['overheadCost']

    return schedule

def SimpleScheduleValidator(schedule,orders):
    validFlag = True
    numOfOrders = 0
    seenOrders = set()
    for queue in schedule['queues']:
        truck = queue['truck']
        for run in queue['runs']:
            if len(run['orders']) > truck['maxOrdersPerRun']:
                validFlag = False

            runQuantity = run['quantity']
            for order in run['orders']:
                numOfOrders += 1
                if order['id'] in seenOrders:
                    validFlag = False
                else:
                    seenOrders.add(order['id'])

            if runQuantity > truck['capacity']:
                validFlag = False

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


'''
print('using randomOptimizer')
exampleSchedule = RandomOptimizer(exampleTrucks,exampleOrders,10000)
print('schedule passes validation? ', SimpleScheduleValidator(exampleSchedule,exampleOrders))
PrettyPrintSchedule(exampleSchedule)
print('total cost of schedule: $',exampleSchedule['totalCost'])
print('total time of schedule: ',exampleSchedule['requiredTime'],'h')
'''

'''
print('using HeuristicRouter')
exampleSchedule = HeuristicRouter(exampleTrucks,exampleOrders)
exampleSchedule = SimpleScheduleEval(exampleSchedule)
print(exampleSchedule)
print('schedule passes validation? ', SimpleScheduleValidator(exampleSchedule,exampleOrders))
print('total cost of schedule: $',exampleSchedule['totalCost'])
print('total time of schedule: ',exampleSchedule['requiredTime'],'h')
'''

'''
print('using RandomRouter')
exampleSchedule = RandomRouter(exampleTrucks,exampleOrders)
exampleSchedule = SimpleScheduleEval(exampleSchedule)
print(exampleSchedule)
print('schedule passes validation? ', SimpleScheduleValidator(exampleSchedule,exampleOrders))
print('total cost of schedule: $',exampleSchedule['totalCost'])
print('total time of schedule: ',exampleSchedule['requiredTime'],'h')
'''
