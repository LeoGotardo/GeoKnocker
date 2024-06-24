from alive_progress import alive_bar, config_handler
from icecream import ic
from modules import *

import requests
import socket
import sys
import os

class PortScan:
    @staticmethod
    def scanPorts(**kwargs):
        os.system('cls' if os.name == 'nt' else 'clear')
        ic(kwargs)

        try:
            validParameters = ['-a', '-m']
            
            if kwargs["port_option"] in validParameters:
                if kwargs["port_option"].lower() == "-a":
                    if "rangePorts" in kwargs:
                        ports = list(range(kwargs['rangePorts'][0], kwargs["rangePorts"][1] + 1))
                    else:
                        ports = list(range(1, 65535))
                    
                if kwargs["port_option"].lower() == "-m":
                    ports = [20, 21, 22, 23, 25, 53, 80, 443, 1194, 3306, 5000, 5432, 8000, 8080, 8291, 8728, 9050]
                    
                openPorts = []
                with alive_bar(len(ports), title="Knocking doors...") as bar:
                    for port in ports:
                        try:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                s.settimeout(0.8)
                                result = s.connect_ex((kwargs["ip"], port))
                                if result == 0:
                                    print(f"[+] {port} --> OPEN")
                                    openPorts.append([port, 'open'])
                                s.close()

                        except socket.error as e:
                            print(f'Error: {e}')
                            return str(e)
                        except KeyboardInterrupt:
                            print('[!] Sniffer interrupted')
                            quit()
                        bar()
                if kwargs['geo'] is not None:
                    locate = geoLocate.getGeo(kwargs['ip'])
                    return openPorts, locate
                else:
                    return openPorts, None
            else:
                error = '[!] The options are -a for all ports, -m for main ports and -g for geolocation!'
                print(error)
                return error, None

        except Exception as e:
            print(f"Error: {e}")
            return str(e), None

class geoLocate:
    @staticmethod
    def getGeo(ip):
        try:
            response = requests.get( f"https://ipinfo.io/{ip}")
            data = response.json()
            
            if 'error' not in data:
                info = {'country': data['country'],
                        'city':data['city'],
                        'lat':data['loc'].split(',')[0],
                        'lon':data['loc'].split(',')[1],
                        'timezone':data['timezone'],
                        'org':data['org'],
                        'hostname':data['hostname']}
                return info
            else:
                error = data['error']
                error = error['message']
                return f"Error: {error}"
        except Exception as e:
            erro = e
            return f"Error: {e}"
    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        port_option = str(sys.argv[2])
        scanner = PortScan()
        scanner.scanPorts(ip, port_option)

    elif len(sys.argv) == 3 or 5 and sys.argv[2].lower() == '-g':
        if sys.argv[3].lower() == '-a':
            ip = sys.argv[1]
            port_option = str(sys.argv[3])
            start_port = int(sys.argv[4])
            end_port = int(sys.argv[5])
            scanner = PortScan()
            scanner.scanPorts(ip, port_option, start_port, end_port)
            locate = geoLocate()
            locate.getGeo(ip)

        elif sys.argv[3].lower() == '-m':
            ip = sys.argv[1]
            port_option = str(sys.argv[3])
            scanner = PortScan()
            scanner.scanPorts(ip, port_option)
            locate = geoLocate()
            locate.getGeo(ip)
        
        else:
            raise ValueError('[!] You must pass -g before the others params if you want to GeoLocate ip address!')


    elif len(sys.argv) == 5 and sys.argv[2].lower() == '-a' and sys.argv[3] == '0':
        print(f'port: {sys.argv[3]} is invalid')

    elif len(sys.argv) == 5 and sys.argv[2].lower() == '-a':
        ip = sys.argv[1]
        port_option = str(sys.argv[2])
        start_port = int(sys.argv[3])
        end_port = int(sys.argv[4])
        scanner = PortScan()
        scanner.scanPorts(ip, port_option, start_port, end_port)
    else:
        print(f"""Usage:\n
                ➜\tpython3 portScanner.py IP_Address -a (for all ports)\n
                ➜\tpython3 portScanner.py IP_Address -a start_port end_port\n
                ➜\tpython3 portScanner.py IP_Address -m (for main ports)\n
                ➜\tpython3 portScanner.py IP_Address -g (for geolocation)""")