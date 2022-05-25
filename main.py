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

kmb_base_url = "https://data.etabus.gov.hk/"

end_point = {}

end_point['route_list'] = "/v1/transport/kmb/route/"
end_point['route'] = "/v1/transport/kmb/route/"

action = {1 : 'route_list',
          2 : 'route',
          3 : 'stop_list',
          4 : 'stop',
          5 : 'route-stop_list',
          6 : 'route-stop',
          7 : 'eta',
          8 : 'stop_eta',
          9 : 'route_eta'}

direction = {1 : 'inbound',
             2 : 'outbound'}



route = '265B'
direction = 'outbound'
service_type = '1'

request_url = kmb_base_url+end_point[action[1]]
# request_url = kmb_base_url+end_point[action[2]]+"/"+route+"/"+direction+"/"+service_type
# request_url = kmb_base_url+"/v1/transport/kmb/stop"

res = requests.get(request_url)

# for route in route_data:
if (res.status_code == 200):
    json_obj = json.loads(res.text)
    for i in range(len(json_obj["data"])):
         print(json_obj["data"][i]['route'])
    # for route in json_obj["data"]:
    #     print(f"{route['route']}\n{route['dest_en']}\n")

    file = open("routelist.csv","w")
    for route in json_obj["data"]:
        file.write(f"{route['route']},{route['dest_en']}\n")
    file.close()



def change_route():
    route = '74B'
    direction = 'outbound'
    service_type = '1'

    request_url = kmb_base_url + end_point[action[2]] + "/" + route + "/" + direction + "/" + service_type

    res = requests.get(request_url)

    route_data = res.json()

    route_no_label = tk.Label(window, text=route_data['data']['route'])
    route_orig_label = tk.Label(window, text=route_data['data']['orig_tc'])
    route_dest_label = tk.Label(window, text=route_data['data']['dest_tc'])
    change_route_button = tk.Button(window, text='265B', command=change_route)



window = tk.Tk()
window.geometry("400x300")
window.title("KMB Route Inquiry")

clicked = StringVar()
clicked.set("route")

route_dropdown_list = tk.OptionMenu(window, clicked, *json_obj['data'][0])
route_dropdown_list.pack()

window.mainloop()

"""

route_no_label = tk.Label(window, text="路線 : "+route_data['data']['route'])
bound_label = tk.Label(window, text=route_data['data']['bound'])
route_orig_label = tk.Label(window,text=route_data['data']['orig_tc'])
route_dest_label = tk.Label(window,text=route_data['data']['dest_tc'])
change_route_button = tk.Button(window, text='74B', command=change_route)


route_no_label.pack()
bound_label.pack()
route_orig_label.pack()
route_dest_label.pack()
change_route_button.pack()


"""