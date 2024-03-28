import requests
import json
from collections import OrderedDict
from operator import getitem


def getRouteData(route_number:int):
    request_url = "https://www3.septa.org/api/TransitView/index.php?route="+str(route_number)
    route = requests.get(request_url)
    route = route.json()
    route_dict = {}

    if route_number == 13:
        lng_min = -75.211
    elif route_number == 11 or route_number == 36:
        lng_min = -75.208
    elif route_number == 34:
        lng_min = -75.212
    
    i=0

    for x in route['bus']:
        if(x['Direction'] == "Eastbound" and x['late'] != 998 and x['late'] != 999 and float(x["lng"])<lng_min):
            temp_dict = {"route_"+str(route_number)+"_trolley_"+str(i):{"trolleyID":x["label"], 
                                           "lateTime": x["late"], 
                                           "tripID": x["trip"],
                                           "direction":x["Direction"],
                                           "blockID":x["BlockID"],
                                           "next_stop_name":x["next_stop_name"],
                                           "next_stop_id":x["next_stop_id"],
                                           "lat":x["lat"],
                                           "long":x['lng'],
                                           "distance":(85*abs(float(x['lng'])-lng_min))
                                           }}
            route_dict.update(temp_dict)
            i += 1
    
    return route_dict


def getTiming(tripID,route):

    if route == 13:
        stopID = 20800
    elif route == 11 or route == 36:
        stopID = 20728
    elif route == 34:
        stopID == 20873

    request_url = "https://www3.septa.org/api/BusSchedules/index.php?stop_id="+str(stopID)

    sched = requests.get(request_url)
    sched = sched.json()

    if route == 13 or route == 34:
        for x in sched:
            


    


route_numbers = [13,11,36,34]

all_routes_dict = {}

for i in range(len(route_numbers)):
    all_routes_dict.update(getRouteData(route_numbers[i]))

print(json.dumps(all_routes_dict,indent = 4))

all_routes_sorted = OrderedDict(sorted(all_routes_dict.items(),
       key = lambda x: getitem(x[1], 'distance')))

# all_routes_list = list(all_routes_sorted.items())

print(json.dumps(all_routes_sorted, indent = 4))

trolleys = len(all_routes_sorted)

print(trolleys)

# print(json.dumps(all_routes_sorted[0], indent=4))





