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

def getAllRouteData():
    request_url = "https://www3.septa.org/api/TransitViewAll/index.php"
    route = requests.get(request_url)
    
    route = route.json()
    route_dict = {}
    temp_dict ={}

    route_numbers = ["T2", "T3", "T4", "T5"]
    for x in route['routes']:
        for route_num in route_numbers:
            i=0
            if route_num in x:
                for y in x[route_num]:
                    if(y['destination'] == "13th-Market" and y['late'] != 998 and y['late'] != 999):
                        if(y['route_id'] == "T3"):
                            stop_lng = -75.209064
                            stop_lat = 39.948379
                        elif(y['route_id'] == "T4" or y['route_id'] == "T5"):
                            stop_lng = -75.208629
                            stop_lat = 39.945328
                        elif(y['route_id'] == "T2"):
                            stop_lng = -75.209273
                            stop_lat = 39.949520

                        if(float(y["lng"])<stop_lng):        
                            temp_dict = {"route_"+y['route_id']+"_trolley_"+str(i):{
                                "trolleyID":y["label"], 
                                "late": y["late"], 
                                "tripID": y["trip"],
                                "direction":y["Direction"],
                                "destination":y["destination"],
                                "blockID":y["BlockID"],
                                "next_stop_name":y["next_stop_name"],
                                "next_stop_id":y["next_stop_id"],
                                "lat":y["lat"],
                                "long":y['lng'],
                                "route_id":y["route_id"],
                                "distance":(geopy.distance.geodesic((stop_lat,stop_lng), (y['lat'], y['lng'])).km),
                                "dist_arrival":math.floor((3*geopy.distance.geodesic((stop_lat,stop_lng), (y['lat'], y['lng'])).km))
                                }}
                            if(temp_dict["route_"+y['route_id']+"_trolley_"+str(i)]["route_id"]=="T5" or 
                               temp_dict["route_"+y['route_id']+"_trolley_"+str(i)]["route_id"]=="T4"):
                                temp_dict["route_"+y['route_id']+"_trolley_"+str(i)]["route_id"]="T4/5"
                        route_dict.update(temp_dict)
                        i += 1                  
    return route_dict

def nearestEachRoute(dict):

    route_arrivals = {"T2":[], "T3":[], "T4/5":[]}

    for key, trolley_info in dict.items():
        route = trolley_info.get("route_id")
        if route == "T3":
            if trolley_info.get("dist_arrival") < 30:
                route_arrivals["T3"].append(trolley_info.get("dist_arrival"))
        elif route == "T4/5":
            if trolley_info.get("dist_arrival") < 30:
                route_arrivals["T4/5"].append(trolley_info.get("dist_arrival"))
        elif route == "T2":
            if trolley_info.get("dist_arrival") < 30:
                route_arrivals["T2"].append(trolley_info.get("dist_arrival"))

    for key, trolley_info in route_arrivals.items():
        trolley_info = trolley_info.sort()
    
    return route_arrivals

def update_time():
    current_time = datetime.datetime.now()
    time_label.config(text=f"Last refreshed: {round((current_time - refresh_time).total_seconds())} seconds ago")

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
            label = tk.Label(popup, text=f"{key} arriving in {str(route)[1:-1]} minutes",
                            font=custom_font, fg='lime green', bg='#222425', anchor='w')
            label.pack(pady=10, padx=10, fill='x')
            trolley_labels.append(label)

    # Schedule the next update after 1 minute (60000 milliseconds)
    popup.after(20000, update_display)

if __name__ == "__main__":
    # Create Tkinter window
    popup = tk.Tk()
    popup.title("Nearest Trolleys")
    popup.configure(bg='#222425')  # Set background color to black
    custom_font = ("Overpass", 48, "bold")

    trolley_labels = []

    # Create label to display time since last refresh
    time_label = tk.Label(popup, text="", font=("Overpass", 18), fg='lime green', bg='#222425')
    time_label.pack(side = "bottom", pady=5)  # Pack the time label initially

    # Initially populate and start updating the display
    refresh_time = datetime.datetime.now()
    update_display()
    update_time()

    # Run the Tkinter event loop
    popup.mainloop()
