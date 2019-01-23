import re
import argparse
from prettytable import PrettyTable
from netmiko import  Netmiko

class Device:
        def writeDB(self, hostname, vendor, model, location):
                with open('devices.db', 'a') as db:
                        db.write(hostname + " " + vendor + " " + model + " " + location + "\n")
        def getDevice(self, hostname):
                with open('devices.db', 'r') as db:
                        device = db.readlines()
                        for i in device:
                                matchObj = re.search(hostname, i, re.I)
                                if matchObj:
                                        return i.rstrip()
        def getLocation(self, location):
                with open('devices.db', 'r') as db:
                        device = db.readlines()
                        for i in device:
                                matchObj = re.search(location, i, re.I)
                                if matchObj:
                                        return i.rstrip()
        def listDevices(self):
                devArr = []
                x = PrettyTable()
                x.field_names = ["Hostname", "Vendor", "Model", "Location", "Device_OS"]
                with open('devices.db', 'r') as db:
                        device = db.readlines()
                        for i in device:
                                devArr = i.split(" ")
                                x.add_row([devArr[0], devArr[1], devArr[2], devArr[3], devArr[4].rstrip()])
                return x


class Login:
        def ciscoIosLogin(self, hostname):
                ciscoIos = {
			"host": hostname,
			"username": username,
			"password": getpass(),
			"device_type": "cisco_ios",
			}
                net_connect = Netmiko(**ciscoIos)
                print(net_connect.find_prompt())
                net_connect.disconnect()

        def juniperLogin(self, hostname):
                junos = {
			"host": hostname,
			"username": username,
			"password": getpass(),
			"device_type": "JuniperSSH",
			}
                net_connect = Netmiko(**junos)
                print(net_connect.find_prompt())
                net_connect.disconnect()

        def linuxLogin(self, hostname:
                linux = {
			"host": hostname,
			"username": "username",
			"password": getpass(),
			"device_type": "LinuxSSH",
			}
                net_connect = Netmiko(**linux)
                print(net_connect.find_prompt())
                net_connect.disconnect()

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
                                help='Add a new device to Database. Entry is space seperated .eg hostname vendor model location os_type')
        parser.add_argument('--login', metavar='N', type=str, nargs='+',
                                help='Login to device using the hostname.')
        args = parser.parse_args()
        if args.list:
                print(dev.listDevices())
        if args.hostname:
                for host in args.hostname:
                        print(dev.getDevice(host))
        if args.location:
                for location in args.location:
                        print(dev.getLocation(location))
        if args.add_device:
                devArr = []
                for device in args.add_device:
                        newDevice = device.split(" ")
                        devArr.append(newDevice[0])
                print(dev.writeDB(devArr[0], devArr[1], devArr[2], devArr[3], devArr[4]))
        if args.login:
                login = Login()
                devArr = []
                for host in args.login:
                        print(dev.getDevice(host))
                        devStr = dev.getDevice(host)
                        devArr = devStr.split(" ")
                        print(devArr)
                        if devArr[4] == "linux":
                                login.linuxLogin(host)
