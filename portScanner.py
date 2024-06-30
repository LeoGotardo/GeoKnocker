from alive_progress import alive_bar, config_handler
from icecream import ic
import requests
import socket
import sys
import os


import socket
import requests
import os
from alive_progress import alive_bar

class PortScan:
    @staticmethod
    def scanPorts(kwargs):
        os.system('cls' if os.name == 'nt' else 'clear')

        try:
            addr_info = socket.getaddrinfo(kwargs['ip'], None)
            ip_address = addr_info[0][4][0]
            print(f"IP Address: {ip_address}\n")
            validParameters = ['-a', '-m']

            if kwargs["port_option"] in validParameters:
                if kwargs["port_option"].lower() == "-a":
                    if "rangePorts" in kwargs:
                        ports = list(range(kwargs['rangePorts'][0], kwargs["rangePorts"][1] + 1))
                    else:
                        ports = list(range(1, 65535))

                elif kwargs["port_option"].lower() == "-m":
                    ports = [20, 21, 22, 23, 25, 53, 80, 443, 1194, 3306, 5000, 5432, 8000, 8080, 8291, 8728, 9050]

                openPorts = []
                with alive_bar(len(ports), title="Knocking doors...") as bar:
                    for port in ports:
                        try:
                            family = addr_info[0][0]
                            with socket.socket(family, socket.SOCK_STREAM) as s:
                                s.settimeout(0.8)
                                result = s.connect_ex((ip_address, port))
                                if result == 0:
                                    openPorts.append([port, 'OPEN'])
                                s.close()

                        except socket.error as e:
                            print(f'Error: {e}')
                            return [e, None]
                        except KeyboardInterrupt:
                            print('[!] Sniffer interrupted')
                            quit()
                        bar()
                if 'geo' in kwargs:
                    locate = geoLocate.getGeo(ip_address)
                    return [openPorts, locate]
                else:
                    return [openPorts, None]
            else:
                error = '[!] The options are -a for all ports, -m for main ports and -g for geolocation!'
                return [error, None]

        except Exception as e:
            print(f"Error: {e}")
            return [e, None]

class geoLocate:
    @staticmethod
    def getGeo(ip):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
            data = response.json()

            if 'error' not in data:
                info = {
                    'country': data.get('country', 'N/A'),
                    'city': data.get('city', 'N/A'),
                    'lat': data.get('loc', '0,0').split(',')[0],
                    'lon': data.get('loc', '0,0').split(',')[1],
                    'timezone': data.get('timezone', 'N/A'),
                    'org': data.get('org', 'N/A'),
                    'hostname': data.get('hostname', 'N/A')
                }
                return info
            else:
                error = data['error']
                error = error['message']
                return f"[!] Error: {error}"
        except Exception as e:
            return f"[!] Error: {e}"




if __name__ == '__main__':
    kwargs = {}
    items = []
    i = 1
    
    try:
        kwargs['ip'] = sys.argv[1]
        for i in range(len(sys.argv)):
            if sys.argv[i].isdigit():
                items.append(int(sys.argv[i]))
                
        if len(items) == 2:
            kwargs['rangePorts'] = items
        if '-a' in sys.argv:
            kwargs['port_option'] = '-a'
        if '-m' in sys.argv:
            kwargs['port_option'] = '-m'
        if '-g' in sys.argv:
            kwargs['geo'] = '-g'
    except Exception as e:
        print(f"""Error: {e}\n
                Usage:\n
                ➜\tpython3 portScanner.py IP_Address -a (for all ports)\n
                ➜\tpython3 portScanner.py IP_Address -a start_port end_port\n
                ➜\tpython3 portScanner.py IP_Address -m (for main ports)\n
                ➜\tpython3 portScanner.py IP_Address -g (for geolocation)""")
        exit()
    try:
        result = PortScan.scanPorts(kwargs)
        location = result[1]
        print("\nPorts:")
        for port in result[0]:
            print(f"{port[0]} --> {port[1]}")
        print("\n")
        if location is not None:
            formatedLocation = f"""Geolocation Information:
            ------------------------------------------------
            Country:      {location.get('country', 'N/A')}
            City:         {location.get('city', 'N/A')}
            Latitude:     {location.get('lat', 'N/A')}
            Longitude:    {location.get('lon', 'N/A')}
            Timezone:     {location.get('timezone', 'N/A')}
            Organization: {location.get('org', 'N/A')}
            Hostname:     {location.get('hostname', 'N/A')}
            ------------------------------------------------"""
        else:
            formatedLocation = f"""Geolocation Information:
            ------------------------------------------------
            Error: {location}
            ------------------------------------------------"""
        
        print(formatedLocation)
    except Exception as e:
        print(f"Error: {e}")