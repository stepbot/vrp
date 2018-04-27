import vrp
import json

with open('data/orders.json') as infile:
    orders = json.load(infile)

with open('data/trucks.json') as infile:
    trucks = json.load(infile)


schedule = vrp.RandomRouter(trucks,orders)
simulatedSchedule = vrp.SimpleScheduleRunner(schedule,True)

print('schedule passes validation? ', vrp.SimpleScheduleValidator(simulatedSchedule,orders))
vrp.PrettyPrintSimulatedSchedule(simulatedSchedule)
print('total cost of schedule: $',simulatedSchedule['totalCost'])
print('total time of schedule: ',simulatedSchedule['requiredTime'],'h')
