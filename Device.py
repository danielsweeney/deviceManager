import re
import argparse
from prettytable import PrettyTable

class Device:
        def __init__(self):
                count = 1
        def writeDB(self, hostname, vendor, model, location):
                with open('devices.db', 'a') as db:
                        db.write(hostname + " " + vendor + " " + model + " " + location + "\n")
        def getDevice(self, hostname):
                with open('devices.db', 'r') as db:
                        device = db.readlines()
                        for i in device:
                                matchObj = re.search(hostname, i, re.I)
                                if matchObj:
                                        print (i.rstrip())
        def getLocation(self, location):
                with open('devices.db', 'r') as db:
                        device = db.readlines()
                        for i in device:
                                matchObj = re.search(location, i, re.I)
                                if matchObj:
                                        print (i.rstrip())
        def listDevices(self):
                devArr = []
                x = PrettyTable()
                x.field_names = ["Hostname", "Vendor", "Model", "Location"]
                with open('devices.db', 'r') as db:
                        device = db.readlines()
                        for i in device:
                                devArr = i.split(" ")
                                x.add_row([devArr[0], devArr[1], devArr[2], devArr[3].rstrip()])
                print(x)

if __name__ == '__main__':
        dev = Device()
        parser = argparse.ArgumentParser(description='Manage device inventory.')
        parser.add_argument('--list', metavar='N', type=str,
                                help='List all devices in inventory.')
        parser.add_argument('--hostname', metavar='N', type=str, nargs='+',
                                help='Search by device hostname.\nAccepts Multiple space seperated entries.\n')
        parser.add_argument('--location', metavar='N', type=str, nargs='+',
                                help='List devices by Location. - Uses the 3 letter identifier e.g. DUB.\nAccepts Multiple space seperated entries\n')
        parser.add_argument('--add_device', metavar='N', type=str, nargs='+',
                                help='Add a new device to Database. Entry is space seperated .eg hostname vendor model location')
        args = parser.parse_args()
        if args.list:
                dev.listDevices()
        if args.hostname:
                for host in args.hostname:
                        dev.getDevice(host)
        if args.location:
                for location in args.location:
                        dev.getLocation(location)
        if args.add_device:
                devArr = []
                for device in args.add_device:
                        newDevice = device.split(" ")
                        devArr.append(newDevice[0])
                dev.writeDB(devArr[0], devArr[1], devArr[2], devArr[3])
