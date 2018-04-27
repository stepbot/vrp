from random import randint,uniform,shuffle,choice
from math import sqrt,inf,exp
from operator import itemgetter
from collections import deque
from copy import deepcopy


def OrderGenerator(numOfOrders,quantityLimit,distanceLimit):
    deliveryWindowStartLimit = 7
    deliveryWindowEndLimit = 17
    deliveryWindowLengthMinLimit = 2
    deliveryWindowLengthMaxLimit = deliveryWindowEndLimit-deliveryWindowStartLimit
    orders = []
    for i in range(numOfOrders):
        order = {}
        order['id']=i
        order['quantity']=randint(1,quantityLimit)
        order['x']=uniform(0,distanceLimit)
        order['y']=uniform(0,distanceLimit)
        order['timeWindowLength']=randint(deliveryWindowLengthMinLimit,deliveryWindowLengthMaxLimit)
        order['timeWindowStart']=randint(deliveryWindowStartLimit,deliveryWindowEndLimit-order['timeWindowLength'])
        order['timeWindowEnd']=order['timeWindowStart']+order['timeWindowLength']


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

def TemporalConsistencyCheck(run,checkOrder):
    validFlag = True
    if len(run['orders'])>0:
        if checkOrder['timeWindowEnd'] < run['orders'][-1]['timeWindowStart']:
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
                    if order['servedAt'] > order['timeWindowEnd']:
                        print('\t\tOrder ',order['id'],' of ',order['quantity'],' units served late @ ',order['servedAt'])

                    elif order['servedAt'] < order['timeWindowStart']:
                        print('\t\tOrder ',order['id'],' of ',order['quantity'],' units served early @ ',order['servedAt'])

                    else:
                        print('\t\tOrder ',order['id'],' of ',order['quantity'],' units served on time @ ',order['servedAt'])







def RandomRouter(trucks,orders):
    schedule = {}
    schedule['queues'] = []
    schedule['directCost'] = inf
    schedule['oppurtunityCost'] = inf
    schedule['totalCost'] = inf
    schedule['requiredTime'] = inf
    schedule['truckStartTime'] = 7
    schedule['speed'] = 45
    schedule['overheadCostRate'] = 270
    schedule['lateTimeErrorCostRate'] = 3*schedule['overheadCostRate']
    schedule['earlyTimeErrorCostRate'] = 2*schedule['overheadCostRate']


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

                validOrder = False
                if (CapacityCheck(workingRun,workingOrder) and TemporalConsistencyCheck(workingRun,workingOrder)):
                    validOrder = True


                if validOrder:
                    workingRun['orders'].append(workingOrder)
                    workingRun['quantity'] += workingOrder['quantity']
                else:
                    workingOrders.appendleft(workingOrder)
            else:
                workingOrder = workingOrders.pop()

                validOrder = False
                if (CapacityCheck(workingRun,workingOrder) and TemporalConsistencyCheck(workingRun,workingOrder)):
                    validOrder = True

                if validOrder:
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
        queue['runs'] = []
        queue['directCost'] = inf
        queue['oppurtunityCost'] = inf
        queue['totalCost'] = inf
        queue['requiredTime'] = inf
        schedule['queues'].append(queue)

    shuffle(runs)

    for queue in schedule['queues']:
        for run in runs:
            run['orders'] = list(run['orders'])
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


def SimpleScheduleRunner(schedule,verbose):
    # function to simulate a given schedule

    simulatedSchedule = deepcopy(schedule)

    # cost tracking variables for schedulewide tracking
    simulatedSchedule['directCost'] = 0.0
    simulatedSchedule['oppurtunityCost'] = 0.0
    simulatedSchedule['overheadCost'] = 0.0
    simulatedSchedule['errorCost'] = 0.0
    simulatedSchedule['totalCost'] = 0.0
    simulatedSchedule['errorTime'] = 0.0

    for queue in simulatedSchedule['queues']:
        # iterate through each queue in schedule and simulate each run

        # cost tracking variables for per queue tracking
        queue['directCost'] = 0.0
        queue['oppurtunityCost'] = 0.0
        queue['errorCost'] = 0.0
        queue['totalCost'] = 0.0
        queue['requiredTime'] = 0.0
        queue['errorTime'] = 0.0

        # set current truck
        truck = queue['truck']

        if verbose:
            print('truck #{0:d}'.format(truck['id']))

        # run numbering as runs are not uniquely numbered
        ii = 0

        for run in queue['runs']:
            # iterate through each  run in queue and simulate

            # cost tracking variables for per run tracking
            run['directCost'] = 0.0
            run['oppurtunityCost'] = 0.0
            run['errorCost'] = 0.0
            run['totalCost'] = 0.0
            run['requiredTime'] = 0.0
            run['errorTime'] = 0.0


            # penalty for over capacity runs
            if run['quantity'] > truck['capacity']:
                # penalty multiplier starting at 10 and rising exponetially with excess quantity served
                run['costMultiplier'] = 10*exp(run['quantity']-truck['capacity'])
            else:
                run['costMultiplier'] = 1

            if verbose:
                print('\tstarts run #{0:d}'.format(ii))
                print('\t\tdeparts home at ({0:5.2f},{1:5.2f},{2:5.2f})'.format(truck['x'],truck['y'],truck['time']))

            # iterate run numbering

            ii += 1

            for order in run['orders']:
                # iterate through each order in the run and simulate

                # distance from current truck position to order location
                marginalDistance = DistanceBetween(truck['x'],truck['y'],order['x'],order['y'])

                # time required to travel from current location to order location
                marginalTime = (marginalDistance/schedule['speed'])

                # update truck state variables to fulfill order
                truck['x'] = order['x']
                truck['y'] = order['y']
                truck['time'] += marginalTime

                # note temporal effects of fulfilling order where necessary
                order['servedAt'] = truck['time']
                run['requiredTime'] += marginalTime
                queue['requiredTime'] += marginalTime

                # check if order was served on time and apply necessary penalties
                if truck['time'] > order['timeWindowEnd']:
                    # if truck is late

                    # accumulate total error time
                    run['errorTime'] += truck['time']-order['timeWindowEnd']
                    queue['errorTime'] += run['errorTime']

                    # caclculate of being late
                    run['errorCost'] += run['errorTime']*simulatedSchedule['lateTimeErrorCostRate']

                elif truck['time'] < order['timeWindowStart']:
                    # if truck is early

                    # accumulate total error time
                    run['errorTime'] += order['timeWindowStart']-truck['time']
                    queue['errorTime'] += run['errorTime']

                    # caclculate of being early
                    run['errorCost'] += run['errorTime']*simulatedSchedule['earlyTimeErrorCostRate']

                else:
                    # hopefully only when on time
                    run['errorCost'] = 0
                    run['errorTime'] += 0
                    queue['errorTime'] += 0

                if verbose:
                    print('\t\tarrives at order #{0:d} at ({1:5.2f},{2:5.2f},{3:5.2f})'.format(order['id'],truck['x'],truck['y'],truck['time']))

                # note temporal effects of unloading order where necessary
                truck['time'] += truck['unloadTime']
                queue['requiredTime'] += truck['unloadTime']
                run['requiredTime'] += truck['unloadTime']

            # run complete so simulate return to base
            # distance from current truck position to base location
            marginalDistance = DistanceBetween(truck['x'],truck['y'],truck['homeX'],truck['homeY'])
            # time required to travel from current location to base location
            marginalTime = (marginalDistance/simulatedSchedule['speed'])

            # update truck state variables to return to base
            truck['x'] = order['x']
            truck['y'] = order['y']
            truck['time'] += marginalTime

            # note temporal effects of returning to base
            queue['requiredTime'] += marginalTime
            run['requiredTime'] += marginalTime

            if verbose:
                print('\t\tarrives at home at ({0:5.2f},{1:5.2f},{2:5.2f})'.format(truck['x'],truck['y'],truck['time']))

            # prepare truck for next run
            truck['time'] += truck['turnAroundTime']
            queue['requiredTime'] += truck['turnAroundTime']
            run['requiredTime'] += truck['turnAroundTime']

            # calculate costs
            # direct cost is actual incured cost to operate truck with penalty for being overcapacity
            run['directCost'] = run['costMultiplier']*run['requiredTime']*int(truck['cost'])

            # oppurtunity cost is a fraction of the the direct cost of the run allocated in proportion to the underutilized capacity on truck
            if run['costMultiplier'] != 1:
                # only oppurtunity cost when not overcapacity
                run['oppurtunityCost'] = run['directCost']*((truck['capacity']-run['quantity'])/truck['capacity'])
            else:
                run['oppurtunityCost'] = 0

            # combine run cost contributers
            run['totalCost'] = run['directCost']+run['oppurtunityCost']+run['errorCost']

            # accumulate error time to schedule
            simulatedSchedule['errorTime']+= queue['errorTime']

            # accumulate run costs to queue
            queue['directCost'] += run['directCost']
            queue['oppurtunityCost'] += run['oppurtunityCost']
            queue['errorCost'] += run['errorCost']
            queue['totalCost'] += run['totalCost']

            # accumulate run costs to schedule
            simulatedSchedule['directCost']+= run['directCost']
            simulatedSchedule['oppurtunityCost']+= run['oppurtunityCost']
            simulatedSchedule['errorCost']+= run['errorCost']
            simulatedSchedule['totalCost']+= run['totalCost']

    # check for longest time taken by any schedule and set as schedule time
    maxTime = 0.0
    for queue in simulatedSchedule['queues']:
        if queue['requiredTime'] > maxTime:
            maxTime = queue['requiredTime']

    simulatedSchedule['requiredTime'] =  maxTime

    # calculate overhead cost of operation of the schedule
    simulatedSchedule['overheadCost'] = simulatedSchedule['requiredTime']*simulatedSchedule['overheadCostRate']

    # apply overhead to schedule total
    simulatedSchedule['totalCost'] += simulatedSchedule['overheadCost']

    return simulatedSchedule


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

def RandomOptimizer(trucks,orders,attempts,verbose):
    canidateSchedules = []
    bestCost = inf
    bestSchedule = SimpleScheduleRunner(RandomRouter(trucks,orders),False)
    for ii in range(attempts):
        if ii%1000 == 0:
            if verbose:
                print('RandomOptimizer testing iteration # {0:d}'.format(ii))
        canidateSchedules.append(SimpleScheduleRunner(RandomRouter(trucks,orders),False))

    if verbose:
        print('comparing canidate schedules')

    for schedule in canidateSchedules:
        if schedule['totalCost'] < bestCost:
            bestSchedule = schedule
            bestCost = schedule['totalCost']
            if verbose:
                print('\tRandomOptimizer cost {0:.2f}'.format(bestCost))

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
