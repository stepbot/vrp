import json
import vrp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v","--verbose",help="increase output verbosity",action="store_true")
parser.add_argument("-o","--orders",type=argparse.FileType('r'),help="orders to be scheduled as a json file")
parser.add_argument("-t","--trucks",type=argparse.FileType('r'),help="trucks to be scheduled as a json file")
parser.add_argument("-i","--iterations",type=int,nargs='?',const=1000,default=1000,help="number of iterations to run")
args = parser.parse_args()

orders = json.load(args.orders)
trucks = json.load(args.trucks)

schedule = vrp.RandomOptimizer(trucks,orders,args.iterations)

if args.verbose:
    print('schedule passes validation? ', vrp.SimpleScheduleValidator(schedule,orders))
    vrp.PrettyPrintSchedule(schedule)
    print('total cost of schedule: $',schedule['totalCost'])
    print('total time of schedule: ',schedule['requiredTime'],'h')

with open('data/schedule.json','w') as outfile:
    json.dump(schedule,outfile)
