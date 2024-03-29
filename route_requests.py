import requests
import json
from collections import OrderedDict
from operator import getitem
import geopy.distance
import time

def getRouteDatabyRoute(route_number:int):
    request_url = "https://www3.septa.org/api/TransitView/index.php?route="+str(route_number)
    route = requests.get(request_url)
    route = route.json()
    route_dict = {}

    if route_number == 13:
        stop_lng = -75.211
        stop_lat = 39.947
    elif route_number == 11 or route_number == 36:
        stop_lng = -75.208
        stop_lat = 39.945
    elif route_number == 34:
        stop_lng = -75.212
        stop_lat = 39.949
    
    i=0

    for x in route['bus']:
        if(x['Direction'] == "Eastbound" and x['late'] != 998 and x['late'] != 999 and float(x["lng"])<stop_lng):
            temp_dict = {"route_"+str(route_number)+"_trolley_"+str(i):{"trolleyID":x["label"], 
                                           "lateTime": x["late"], 
                                           "tripID": x["trip"],
                                           "direction":x["Direction"],
                                           "blockID":x["BlockID"],
                                           "next_stop_name":x["next_stop_name"],
                                           "next_stop_id":x["next_stop_id"],
                                           "lat":x["lat"],
                                           "long":x['lng'],
                                           "distance":(geopy.distance.geodesic((stop_lat,stop_lng), (x['lat'], x['lng'])).km)
                                           }}
            route_dict.update(temp_dict)
            i += 1
    
    return route_dict

def getAllRouteData():
    request_url = "https://www3.septa.org/api/TransitViewAll/index.php"
    route = requests.get(request_url)
    
    route = route.json()
    # print(json.dumps(route, indent=4))
    route_dict = {}
    temp_dict ={}

    route_numbers = ["11", "13", "34", "36"]
    for x in route['routes']:
        for route_num in route_numbers:
            i=0
            if route_num in x:
                for y in x[route_num]:
                    if(y['Direction'] == "EastBound" and y['late'] != 998 and y['late'] != 999):
                        if(y['route_id'] == "13"):
                            stop_lng = -75.211
                            stop_lat = 39.947
                        elif(y['route_id'] == "11" or y['route_id'] == "36"):
                            stop_lng = -75.208
                            stop_lat = 39.945
                        elif(y['route_id'] == "34"):
                            stop_lng = -75.212
                            stop_lat = 39.949

                        if(float(y["lng"])<stop_lng):        
                            temp_dict = {"route_"+y['route_id']+"_trolley_"+str(i):{
                                "trolleyID":y["label"], 
                                "lateTime": y["late"], 
                                "tripID": y["trip"],
                                "direction":y["Direction"],
                                "blockID":y["BlockID"],
                                "next_stop_name":y["next_stop_name"],
                                "next_stop_id":y["next_stop_id"],
                                "lat":y["lat"],
                                "long":y['lng'],
                                "route_id":y["route_id"],
                                "distance":(geopy.distance.geodesic((stop_lat,stop_lng), (y['lat'], y['lng'])).km),
                                "est_arrival":(4.2857*geopy.distance.geodesic((stop_lat,stop_lng), (y['lat'], y['lng'])).km)
                                }}
                        route_dict.update(temp_dict)
                        i += 1
    return route_dict

def getTiming(trolley_dict):

    i=0

    for key, value in trolley_dict.items():
        if key.startswith("route_"):
         
         if value.get("route_id") == "13":
            stopID = 20800
            print(stopID)
         elif value.get("route_id") == "11" or value.get("route_id") == "36":
            stopID = 20728
            print(stopID)
         elif value.get("route_id") == "34":
            stopID = 20873
            print(stopID)

         request_url = "https://www3.septa.org/api/BusSchedules/index.php?stop_id="+str(stopID)
         sched = requests.get(request_url)
         sched = sched.json()
         print(json.dumps(sched, indent = 4))

    return 


#By single route API call
# route_numbers = [13,11,36,34]

# all_routes_dict = {}

# for i in range(len(route_numbers)):
#     all_routes_dict.update(getRouteDatabyRoute(route_numbers[i]))

# all_routes_sorted = OrderedDict(sorted(all_routes_dict.items(),
#        key = lambda x: getitem(x[1], 'distance')))

# all_routes_sorted["trolleyCount"] = len(all_routes_sorted)

# with open('by_route_data_3.json', 'w') as f:
#   json.dump(all_routes_sorted, f, ensure_ascii=False)


#By TransitViewAll API call

all_transit = OrderedDict(sorted(getAllRouteData().items(),
     key = lambda x: getitem(x[1],'distance')))

all_transit['trolleyCount'] = len(all_transit)

with open('all_route_data_3.json', 'w') as f:
  json.dump(all_transit, f, ensure_ascii=False)


getTiming(all_transit)



