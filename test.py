import requests



#url = "https://10.64.65.43/webglue/isw/status"

url = "https://10.64.65.43/webglue/rawcontent?timedRefresh=1&c=Status&lang=en"

response = requests.get(url, verify=False)

json_data = response.json()


Tray = ""
#url = "http://" + self.name +"/webglue/rawcontent?timedRefresh=1&c=Status&lang=en"
trays=[]            
           
if json_data == "":
    self.trays = []
            # trays = json_data["nodes"]['inputs']
else:
    inputs = json_data["nodes"]['inputs']
    i = 0
        #  "inputs" : {
        # "Tray 1" : {
            # "capacity" : 500,
        # "},
        # "Tray 2" : {
            # "capacity" : 500,
            # }
            # }

    for tray in inputs:
        tray_obj = ""
        if tray.startswith("Tray"):
            tray_obj.name = tray['name']
            earlyWarning = inputs[tray_obj.name]['levelInfo']['earlyWarningLevel']
            
            print(tray_obj)
