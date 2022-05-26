"""
KMB API Data Dictionary:
https://data.etabus.gov.hk/datagovhk/kmb_eta_data_dictionary.pdf

KMB API Specification:
https://data.etabus.gov.hk/datagovhk/kmb_eta_api_specification.pdf
"""

import requests
import tkinter as tk
from tkinter import StringVar
import json
from gui import *

# KMB API Base URL
kmb_base_url = "https://data.etabus.gov.hk/"

# Provide Functions in KMB API
action = {
    1 : 'route_list',
    2 : 'route',
    3 : 'stop_list',
    4 : 'stop',
    5 : 'route-stop_list',
    6 : 'route-stop',
    7 : 'eta',
    8 : 'stop_eta',
    9 : 'route_eta'}

end_point = {}
end_point[action[1]] = "/v1/transport/kmb/route/"
end_point[action[2]] = "/v1/transport/kmb/route/"
"""/v1/transport/kmb/stop
/v1/transport/kmb/stop
/v1/transport/kmb/route-stop
/v1/transport/kmb/route-stop
/v1/transport/kmb/eta/{stop_id}/{route}/{service_type}
/v1/transport/kmb/stop-eta/{stop_id}
/v1/transport/kmb/route-eta/{route}/{service_type}
"""

direction = {1 : 'inbound',
             2 : 'outbound'}



route = '265B'
direction = 'outbound'
service_type = '1'

request_url = kmb_base_url+end_point[action[1]]
# request_url = kmb_base_url+end_point[action[2]]+"/"+route+"/"+direction+"/"+service_type
# request_url = kmb_base_url+"/v1/transport/kmb/stop"

res = requests.get(request_url)

route_list = []
# for route in route_data:
if (res.status_code == 200):
    json_obj = json.loads(res.text)
    for i in range(len(json_obj["data"])):
        route_list.append(json_obj['data'][i]['route'])

    print(route_list)

    # for route in json_obj["data"]:
    #     print(f"{route['route']}\n{route['dest_en']}\n")

    file = open("routelist.csv","w")
    for route in json_obj["data"]:
        file.write(f"{route['route']}, {route['dest_en']}\n")
    file.close()


def view_details_action1():
    route_orig_label.config(text="Done")
    route_dest_label.config(text="Destination")

def view_details_action2(choice):
    route_orig_label.config(text=choice)
    route_dest_label.config(text="Destination")

window = tk.Tk()
window.geometry("400x300")
window.title("KMB Route Inquiry")

firstRouteOfList = StringVar()
firstRouteOfList.set(route_list[0])

route_no_label = tk.Label(window, text="路線 : ")
route_no_label.pack(expand=True)
route_dropdown_list = tk.OptionMenu(window, firstRouteOfList, *route_list, command=view_details_action2)
route_dropdown_list.pack(expand=True)
view_details_button = tk.Button(window, text='View Details', command=view_details_action1)
view_details_button.pack(expand=True)
route_orig_label = tk.Label(window, text="")
route_dest_label = tk.Label(window, text="")
route_orig_label.pack(expand=True)
route_dest_label.pack(expand=True)

window.mainloop()