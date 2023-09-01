from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import requests
from urllib.request import urlopen
from django.http import FileResponse
import selenium
import re
from bs4 import BeautifulSoup
import json
import os
import pygame 

# Create your views here.

# load the printers
PrinterList = [] 
URLTopbar = ".internal/cgi-bin/dynamic/topbar.html"
URLStatus = ".internal/cgi-bin/dynamic/printer/PrinterStatus.html"

printers_list = "../Printers.txt"

oldModelList = ['Lexmark XS955', 'Lexmark XS864', 'Lexmark XM3150', 'Lexmark XM7155', 'Lexmark XM9155','Lexmark X954','Lexmark X864de','Lexmark XM7155','Lexmark M5155','Lexmark MX410de','Lexmark CS510de','Lexmark C734']
newModelList = ['Lexmark XC9255','Lexmark XC4140']


didLoad = False

class Tray:
    def __init__(self):
        self.name= ""
        self.status = ""
        self.capacity = ""
        self.size = ""
        self.tray_type = ""

class Printer:
    def __init__(self):
        self.session = requests.Session()
        self.isColor = False
        self.html= ""
        self.model=""
        self.name = ""
        self.url_topbar = ".internal/cgi-bin/dynamic/topbar.html"
        self.url_status = ".internal/cgi-bin/dynamic/printer/PrinterStatus.html"
        self.printer_status = ""
        self.location = ""
        self.address = ""
        self.toner_status = ""
        self.toner_percentage = ""
        self.trays = []

        self.cyan_cartridge = ""
        self.magenta_cartridge = ""
        self.yellow_cartridge = ""
        self.black_cartridge =""

    def get_url_topbar(self):
        if self.address != "":
            print("Address: " + self.address)
            return "http://"+self.address + "/cgi-bin/dynamic/topbar.html"
        return "http://"+self.name + self.url_topbar

    def get_url_status(self):
        if self.address != "":
            return "http://"+self.address + "/cgi-bin/dynamic/printer/PrinterStatus.html"
        return "http://"+self.name + self.url_status

    def getHtml(self, url):
        try:
            response = self.session.get(url, timeout=5)
            if response.status_code ==200:
                page = urlopen(url)
                html_bytes = page.read()
                html = html_bytes.decode("utf-8")
                self.html = html
        except requests.exceptions.RequestException as e:
            self.html = ""
            self.status = "Network Error: " + str(e)
            self.status_colour = 0b001000
        return self.html

    def getJson(self, url):
        response = requests.get(url, verify=False)
        return response.json()
    
    def update(self):
        self.getStatus()
        if self.model in oldModelList:
            self.getLocaton()
        if self.address == "":
            if self.model in oldModelList:
                self.getAddress()
        if self.model in oldModelList:        
            self.getTonerPercentage()

        if self.toner_percentage == "" or self.toner_percentage == "Couldn\'t find toner percentage":
            self.isColor = True
            self.getCatridges()
        if self.cyan_cartridge == "Couldn't find cyan cartridge" and self.magenta_cartridge == "Couldn't find magenta cartridge" and self.yellow_cartridge == "Couldn't find yellow cartridge":
            self.isColor = False
        self.getTrays()





    def getAddress(self):
        if self.model in oldModelList:
            self.getHtml(self.get_url_topbar())
            if self.html == "":
                self.address = "Couldn't find address"
            else:
                soup = BeautifulSoup(self.html, 'html.parser')
                address_tag = soup.find(string=re.compile(r'Address:'))
                if address_tag:
                    self.address = address_tag.split('Address: ')[1].strip()
                else:
                    self.address = "Address not found (error Parsing)"
                    # print('Address not found')
                
        elif self.model in newModelList:
            url = "http://" + self.name 
            self.getHtml(url)
            if self.html == "":
                self.address = "Couldn't find address"
            else:
                soup = BeautifulSoup(self.html, 'html.parser')
                address_tag = soup.find(string=re.compile(r'IP Address:'))
                if address_tag:
                    self.address = address_tag.split('Address: ')[1].strip()
                else:
                    self.address = "Address not found (error Parsing)"
                    # print('Address not found')
        else:
            self.address = "Model not found"
            
        
    def getStatus(self):
        if self.model in oldModelList:
            self.getHtml(self.get_url_topbar())
            if self.html == "":
                self.printer_status = "offline"
            else:
                soup = BeautifulSoup(self.html, 'html.parser')
                status = soup.find('table', class_='statusBox').text.strip()
                self.printer_status = status
        elif self.model in newModelList:
            if self.address != "":
                url = "http://" + self.address +"/webglue/isw/status"
            else:
                url = "http://" + self.name +"/webglue/isw/status"
            # get the json response
            json_data = self.getJson(url)
            if json_data == "":
                self.printer_status = "offline"
            else:
                # parse the json response
                self.status = json_data[0]['IrTitle'].strip()
                self.printer_status = json_data[0]['IrTitle'].strip()
                
    
    def getCatridges(self):
        if self.model in oldModelList:
            self.getHtml(self.get_url_status())
            if self.html == "":
                self.cyan_cartridge = "Couldn't find cyan cartridge"
                self.magenta_cartridge = "Couldn't find magenta cartridge"
                self.yellow_cartridge = "Couldn't find yellow cartridge"
            else:
                try:
                	soup = BeautifulSoup(self.html, 'html.parser')
                	self.cyan_cartridge = soup.find('td', bgcolor="#00ffff")['title']
                	self.magenta_cartridge = soup.find('td', bgcolor="#ff00ff")['title']
                	self.yellow_cartridge = soup.find('td', bgcolor="#ffff00")['title']
                	self.black_cartridge = soup.find('td', bgcolor="#000000")['title']
                except:
                	self.cyan_cartridge = "Couldn't find cyan cartridge"
                	self.magenta_cartridge = "Couldn't find magenta cartridge"
                	self.yellow_cartridge = "Couldn't find yellow cartridge"
        elif self.model in newModelList:
            if self.address != "":
                url = "http://" + self.address +"/webglue/rawcontent?timedRefresh=1&c=Status&lang=en"
            else:
                url = "http://" + self.name +"/webglue/rawcontent?timedRefresh=1&c=Status&lang=en"
            
            json_data = self.getJson(url)

            if json_data == "":
                self.cyan_cartridge = "Couldn't find cyan cartridge"
                self.magenta_cartridge = "Couldn't find magenta cartridge"
                self.yellow_cartridge = "Couldn't find yellow cartridge"
            else:
                supplies = json_data["nodes"]['supplies']
                supplies_to_get = ["Cyan Toner", "Magenta Toner", "Yellow Toner", "Black Toner"]
                for supply_name, supply_details in supplies.items():
                    if supply_name in supplies_to_get:
                        if supply_details['supplyName'] == "Cyan Toner":
                            self.cyan_cartridge = ""+str(supply_details['percentFull'])+"%"
                        elif supply_details['supplyName'] == "Magenta Toner":
                            self.magenta_cartridge = ""+str(supply_details['percentFull'])+"%"
                        elif supply_details['supplyName'] == "Yellow Toner":
                            self.yellow_cartridge = ""+str(supply_details['percentFull'])+"%"
                        elif supply_details['supplyName'] == "Black Toner":
                            self.black_cartridge = ""+str(supply_details['percentFull'])+"%"
                    

    
    def getLocaton(self):

        if self.model in oldModelList:
            self.getHtml(self.get_url_topbar())       
            if self.html == "":
                self.location = "Couldn't find location"
                return
            soup = BeautifulSoup(self.html, 'html.parser')
            location_tag = soup.find(string=re.compile(r'Location:'))
            if location_tag:
                self.location = location_tag.split('Location: ')[1].strip()
            else:
                self.location = "Location not found (error Parsing)"
                print('Location not found')
        elif self.model in newModelList:
            url=""
            if self.address != "":
                url="http://"+self.address+"/#/Status"
            else:
                url="http://"+self.name+"/#/Status"
            self.getHtml(url)
            if self.html=="":
                self.location="Could not find location"
                return 
            soup = BeautifulSoup(self.html,'html.parser')
            location_tag = soup.find(string=re.compile(r'Location:'))
            if location_tag:
                self.location = location_tag.split('Location: ')[1].strip()
            else:
                self.location = "Location not found (error Parsing)"
                print('Location not found')

    
    def getTonerPercentage(self):
        url = self.get_url_status()
        self.getHtml(url)
        
        if not self.html:
            self.toner_percentage = "Couldn't find toner percentage"
            return
        
        soup = BeautifulSoup(self.html, 'html.parser')
        toner_percentage_patterns = [
            re.compile(r'Black Cartridge\s*~(\d+)%'),
            re.compile(r'Black Cartridge\s*(\d+)%'),
            re.compile(r'Black Toner\s*~(\d+)%'),
            re.compile(r'Black Toner\s*(\d+)%')
        ]
        
        for pattern in toner_percentage_patterns:
            toner_percentage_match = pattern.search(str(soup))
            if toner_percentage_match:
                self.toner_percentage = toner_percentage_match.group(1)
                return
        
        self.toner_percentage = "Couldn't find toner percentage"


    def handle_error(self, url, response):
        # if object is connection timeout
        if isinstance(response, requests.exceptions.ConnectTimeout):
            self.html_top_bar = ""
            self.html_status = ""
            self.buffer = ""
            self.status = f"Connection Timeout for URL: {url}"
            self.status_colour = 0b001000
            # print(self.status)
            return
        self.html_top_bar = ""
        self.html_status = ""
        self.buffer = ""
        self.status = f"Network Error: {response.status_code} for URL: {url}"
        self.status_colour = 0b001000
        # print(self.status)

    def getTrays(self):
        if self.model in oldModelList:
            self.getHtml(self.get_url_status())
            if self.html == "":
                self.trays = []
                return
            soup = BeautifulSoup(self.html, 'html.parser')
            # Parse Tray Information
            tray_tables = soup.findAll('table', class_='status_table')
            tray_table = tray_tables[1]
            tray_rows = tray_table.find_all('tr')[1:]

            # Iterate over each tray row
            self.trays = []
            for row in tray_rows:
                columns = row.find_all('td')
                tray_name = columns[0].text.strip()
                if tray_name.startswith("Tray"):
                    tray = Tray()
                    tray.name = tray_name
                    tray.status = columns[1].text.strip()
                    tray.capacity = columns[3].text.strip()
                    tray.size = columns[4].text.strip()
                    tray.tray_type = columns[5].text.strip()
                    self.trays.append(tray)
        elif self.model in newModelList:
            if self.address != "":
                url = "http://" + self.address +"/webglue/rawcontent?timedRefresh=1&c=Status&lang=en"
            else:
                url = "http://" + self.name +"/webglue/rawcontent?timedRefresh=1&c=Status&lang=en"
            
           
            json_data = self.getJson(url)
            if json_data == "":
                self.trays = []
                return
            
            inputs = json_data["nodes"]['inputs']
            self.trays = []
            trays_to_get = ["Tray 1", "Tray 2", "Tray 3", "Tray 4"]
            for tray_name, tray_details in inputs.items():
                if tray_name in trays_to_get:
                    tray_obj = Tray()
                    tray_obj.name = tray_name
                    earlyWarning = tray_details['levelInfo']['earlyWarningLevel']
                    # print(earlyWarning)
                    if tray_details['levelInfo']["currentLevel"] <= earlyWarning and tray_details['levelInfo']["currentLevel"] > 0:
                        tray_obj.status = "Low"
                    elif tray_details['levelInfo']["currentLevel"] == 0:
                        tray_obj.status = "Empty"
                    else:
                        tray_obj.status = "OK"
                    
                    tray_obj.capacity = tray_details['capacity']
                    tray_obj.size = tray_details['sizeString']
                    tray_obj.tray_type = tray_details['typeString']
                    self.trays.append(tray_obj)
            


################################################################################################################
# to load all the printers that are in the printers_list file that is the printers.txt
############################################################################################################
def load():
    # global didLoad
    # if didLoad == True:
    #     return
    # load the printers
    PrinterList = []
    with open(printers_list, "r") as file:
        for line in file:
            if line.strip():
                # add the printer to the list of printers using the name
                printer = Printer()
                newline = line.strip()
                if printer.name.startswith("#"):
                    continue
                else:
                    if newline.__contains__("$") and not newline.startswith("#"):
                        # printer.name = newline.split("$")[0]
                        # remove white spaces
                        # mi-a300b-prn1$Lexmark XS864$10.64.64.160
                        printer.name = newline.split("$")[0].strip()
                        newline = newline.split("$")[1]
                        # if the line has another + then it has the ip address
                        if newline.__contains__("+"):
                            printer.model = newline.split("+")[0].strip()
                            printer.address = newline.split("+")[1].strip()
                        else:
                            printer.model = newline.strip()
                        PrinterList.append(printer)
    print("Loaded printers from file")
    file.close()
    PrinterList.sort(key=lambda x: x.name)
    # didLoad = True
    return PrinterList

############################################################################################################
############################################################################################################
############################################################################################################

# to load a demo printer for testing only

def loadOnce():
    global didLoad
    if didLoad == True:
        return
    # only if printers are not available
    printer = Printer()


    printer.name='mi-b202-prn1'
    printer.printer_status = "Sleep mode"
    printer.printer_location = "Behind staircase"
    printer.printer_address = "102.12.12.12"
    printer.toner_status = "Black Catridge ~93%"
    printer.toner_percentage = "93"
    tray = Tray()
    tray.name = "Tray 1"
    tray.status = "OK"
    tray.capacity = "500"
    tray.size = "11x12"
    tray.tray_type = "Legal"

    printer.trays.append(tray)
   
    PrinterList.append(printer)
    didLoad = True


############################################################################################################
############################################################################################################
############################################################################################################

############################################ INDEX #########################################################

def index(request):
    # loadOnce()
    
    PrinterList = load()

    return render(request, 'index.html')


def getPrinters(request):
    global PrinterList
    printers=[]
    PrinterList = load()
    for printer in PrinterList:
        printers.append(printer.name)
    return JsonResponse({'printers':printers})

############################################################################################################
############################################################################################################
############################################################################################################

############################################ UPDATE ########################################################
# To update the printer status and other information

def update(request):
    if request.method == 'GET':
        try: 
            printer_name = request.GET.get('name', None)
            # find the printer in the list of printers
            try:
                printer_obj = next((x for x in PrinterList if x.name == printer_name), None)
            except:
                return JsonResponse({'error': 'Printer not found, you need to refresh the browser'}, safe=False)

            printer = Printer()

            printer.name = printer_obj.name
            printer.model = printer_obj.model
            printer.address = printer_obj.address
            printer.update()
            if printer.printer_status == "" or printer.printer_status == None:
                printer.printer_status = "Offline"

            x = printer
            traysList = []
            for tray in x.trays:
                traysList.append(tray.__dict__)
            x.trays = traysList
            if x.isColor == True:
                return JsonResponse({'name': x.name, 'status': x.printer_status, 'location': x.location, 'address': x.address, 'toner_status': x.toner_status, 'toner_percentage': x.toner_percentage, 'trays': x.trays, 'cyan_cartridge': x.cyan_cartridge, 'magenta_cartridge': x.magenta_cartridge, 'yellow_cartridge': x.yellow_cartridge,'black_cartridge':x.black_cartridge,'isColor': x.isColor,"traysN": len(x.trays)}, safe=False)
            return JsonResponse({'name': x.name, 'status': x.printer_status, 'location': x.location, 'address': x.address, 'toner_status': x.toner_status, 'toner_percentage': x.toner_percentage, 'trays': x.trays, 'isColor': x.isColor,"traysN": len(x.trays)}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, safe=False)
############################################################################################################
############################################################################################################
############################################################################################################


def audio(request):
    # Replace 'path_to_your_audio_file' with the actual path to your audio file
    # playAudio()
    pygame.mixer.init()
    pygame.mixer.music.load("../alert.mp3")
    pygame.mixer.music.play()
    pygame.event.wait()
    pygame.mixer.music.stop()
    return HttpResponse(status=200)