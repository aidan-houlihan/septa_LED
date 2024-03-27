import requests
import json


def getRouteData(route_number):
    request_url = "https://www3.septa.org/api/TransitView/index.php?route="+str(route_number)
    route = requests.get(request_url)

    route = route.json()

    route_dict = {}

    i=0

    for x in route['bus']:
        if(x['Direction'] == "Eastbound" and x['label'] != 0):
            temp_dict = {"route_"+str(route_number)+"_trolley_"+str(i):{"trolleyID":x["label"], 
                                           "lateTime": x["late"], 
                                           "tripID": x["trip"],
                                           "direction":x["Direction"],
                                           "blockID":x["BlockID"]
                                           }}
            route_dict.update(temp_dict)
            i += 1
    
    return route_dict

route_13_func = getRouteData(36)
print(json.dumps(route_13_func, indent = 4, sort_keys = True))

# route13 = requests.get("https://www3.septa.org/api/TransitView/index.php?route=13")
# route11 = requests.get("https://www3.septa.org/api/TransitView/index.php?route=11")
# route36 = requests.get("https://www3.septa.org/api/TransitView/index.php?route=36")
# route34 = requests.get("https://www3.septa.org/api/TransitView/index.php?route=34")

# route13 = route13.json()
# route11 = route11.json()
# route36 = route36.json()
# route34 = route34.json()

# route13_dict = {}
# route11_dict = {}
# route36_dict = {}
# route34_dict = {}

# i=0
# for x in route13['bus']:
#     if(x['Direction'] == "Eastbound" and x['label'] != 0):
#         temp_dict = {"trolley"+str(i):{"trolleyID":x["label"], "lateTime": x["late"], "tripID": x["trip"],"direction":x["Direction"]}}
#         route13_dict.update(temp_dict)
#         i += 1

# i=0
# for x in route11['bus']:
#     if(x['Direction'] == "Eastbound" and x['label'] != 0):
#         temp_dict = {"trolley"+str(i):{"trolleyID":x["label"], "lateTime": x["late"], "tripID": x["trip"],"direction":x["Direction"]}}
#         route11_dict.update(temp_dict)
#         i += 1

# i=0
# for x in route36['bus']:
#     if(x['Direction'] == "Eastbound" and x['label'] != 0):
#         temp_dict = {"trolley"+str(i):{"trolleyID":x["label"], "lateTime": x["late"], "tripID": x["trip"],"direction":x["Direction"]}}
#         route36_dict.update(temp_dict)
#         i += 1

# i=0
# for x in route34['bus']:
#     if(x['Direction'] == "Eastbound" and x['label'] != 0):
#         temp_dict = {"trolley"+str(i):{"trolleyID":x["label"], "lateTime": x["late"], "tripID": x["trip"],"direction":x["Direction"]}}
#         route34_dict.update(temp_dict)
#         i += 1

# print(json.dumps(route13_dict, indent = 4, sort_keys = True))
# print(json.dumps(route11_dict, indent = 4, sort_keys = True))
# print(json.dumps(route36_dict, indent = 4, sort_keys = True))
# print(json.dumps(route34_dict, indent = 4, sort_keys = True))


