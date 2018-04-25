# vrp

## introduction
vrp is a collection of code related to the vehicle routing problem

data is passed to and from the program using json files.
For an example of file structure see included data folder.

vrp currently supports the capacitated vehicle routing problems without time windows.
Delivery locations are currently accepted as miles from the depot which is assumed to be at coordinates of (0,0)
Delivery truck speed is currently fixed at 45mph based on straight line distance.



## installation
1. download code or clone repository
2. change directory into vrp folder
3. install python
4. call vrpSchedule to schedule your routing problem

e.g.

`yourName-MBP:vrp yourName$ python3 vrpSchedule.py -o data/orders.json -t data/trucks.json -i 10000`

for an explanation of available options call vrpSchedule -h option

```
stephans-MBP:vrp stephan$ python3 vrpSchedule.py -h
usage: vrpSchedule.py [-h] [-v] [-o ORDERS] [-t TRUCKS] [-i [ITERATIONS]]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -o ORDERS, --orders ORDERS
                        orders to be scheduled as a json file
  -t TRUCKS, --trucks TRUCKS
                        trucks to be scheduled as a json file
  -i [ITERATIONS], --iterations [ITERATIONS]
                        number of iterations to run
```
