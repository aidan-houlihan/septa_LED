#!/usr/bin/env python3

import requests
import json
from collections import OrderedDict
from operator import getitem
import geopy.distance
import time
import datetime
from dateutil.parser import parse
import math
import tkinter as tk
from ctypes import windll
import platform


if platform.system() == "Windows":
    windll.shcore.SetProcessDpiAwareness(1)

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
                                "late": y["late"], 
                                "tripID": y["trip"],
                                "direction":y["Direction"],
                                "blockID":y["BlockID"],
                                "next_stop_name":y["next_stop_name"],
                                "next_stop_id":y["next_stop_id"],
                                "lat":y["lat"],
                                "long":y['lng'],
                                "route_id":y["route_id"],
                                "distance":(geopy.distance.geodesic((stop_lat,stop_lng), (y['lat'], y['lng'])).km),
                                "dist_arrival":math.floor((3*geopy.distance.geodesic((stop_lat,stop_lng), (y['lat'], y['lng'])).km))
                                }}
                            if(temp_dict["route_"+y['route_id']+"_trolley_"+str(i)]["route_id"]=="36" or 
                               temp_dict["route_"+y['route_id']+"_trolley_"+str(i)]["route_id"]=="11"):
                                temp_dict["route_"+y['route_id']+"_trolley_"+str(i)]["route_id"]="11&36"
                        route_dict.update(temp_dict)
                        i += 1                  
    return route_dict

def getTiming(trolley_dict):

    i=0

    sched_dict = {}

    for key, trolley in trolley_dict.items():
        
        if key.startswith("route_"):
         
         if trolley.get("route_id") == "13":
            stopID = 20800

         elif trolley.get("route_id") == "11" or trolley.get("route_id") == "36":
            stopID = 20728

         elif trolley.get("route_id") == "34":
            stopID = 20873

         request_url = "https://www3.septa.org/api/BusSchedules/index.php?stop_id="+str(stopID)
         sched = requests.get(request_url)
         sched = sched.json()

         for route in sched:
                for trip in sched[route]:
                    if trolley.get('tripID') == trip.get('trip_id'):
                        trolley['orig_time'] = trip.get('DateCalender')
                        if trolley['orig_time']:
                            trolley['est_arrival_time'] = str(parse(trolley['orig_time']) + datetime.timedelta(minutes = trolley['late']) )
    return trolley_dict

def nearestEachRoute(dict):

    # nearest = {}

    # for key, trolley_info in dict.items():
    #         route = trolley_info.get("route_id")
    #         if route not in nearest:
    #             nearest[route] = trolley_info
    #         else:
    #             if trolley_info["dist_arrival"] < nearest[route]["dist_arrival"]:
    #                 nearest[route] = trolley_info

    # desired_order = ['13', '11&36', '34']

    # # Initialize a dictionary to store the nearest trolley for each route
    # nearest_trolleys_ordered = {}

    # # Iterate through each route in the desired order
    # for route_id in desired_order:
    #     # Check if the route has a nearest trolley
    #     if route_id in nearest:
    #         # Add the nearest trolley for this route to the ordered dictionary
    #         nearest_trolleys_ordered[route_id] = nearest[route_id]

    route_arrivals = {"13":[], "11&36":[], "34":[]}

    for key, trolley_info in dict.items():
        route = trolley_info.get("route_id")
        if route == "13":
            route_arrivals["13"].append(trolley_info.get("dist_arrival"))
        elif route == "11&36":
            route_arrivals["11&36"].append(trolley_info.get("dist_arrival"))
        elif route == "34":
            route_arrivals["34"].append(trolley_info.get("dist_arrival"))

    for key, trolley_info in route_arrivals.items():
        trolley_info = trolley_info.sort()
    
    return route_arrivals

def update_time():
    current_time = datetime.datetime.now()
    time_label.config(text=f"Refreshed: {round((current_time - refresh_time).total_seconds())} seconds ago")

    popup.after(1000, update_time)  # Schedule the update_time function to run every second

def update_display():
    global refresh_time

    nearestTrolleys = nearestEachRoute(getAllRouteData())

    # with open('nearestTrolleys.json', 'w') as f:
    #     json.dump(nearestTrolleys, f, ensure_ascii=False)

    refresh_time = datetime.datetime.now()

    # Update trolley information labels
    for label in trolley_labels:
        label.destroy()
    trolley_labels.clear()

    for key, route in nearestTrolleys.items():
        if(len(route)) != 0:
            label = tk.Label(popup, text=f"Route {key}: in {str(route)[1:-1]}'",
                            font=custom_font, fg='lime green', bg='gray12', anchor='w')
            label.pack(pady=10, padx=10, fill='x')
            trolley_labels.append(label)

    # Schedule the next update after 1 minute (60000 milliseconds)
    popup.after(20000, update_display)

if __name__ == "__main__":
    # Create Tkinter window
    popup = tk.Tk()
    popup.title("Nearest Trolleys")
    popup.configure(bg='gray12')  # Set background color to black
    custom_font = ("Overpass", 48, "bold")

    trolley_labels = []

    # Create label to display time since last refresh
    time_label = tk.Label(popup, text="", font=("Overpass", 18), fg='lime green', bg='gray12')
    time_label.pack(side = "bottom", pady=5)  # Pack the time label initially

    # Initially populate and start updating the display
    refresh_time = datetime.datetime.now()
    update_display()
    update_time()

    # Run the Tkinter event loop
    popup.mainloop()
