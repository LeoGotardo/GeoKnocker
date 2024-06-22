from modules import *
from icecream import ic

import socket
import sys

class PortScan:
    @calc
    @staticmethod
    def scanPorts(ip, port_option, *rangePorts):
        try:
            validParameters = ['-a', '-m']
            
            if port_option in validParameters:
                if port_option.lower() == "-a":
                    if rangePorts:
                        ports = list(range(rangePorts[0], rangePorts[1] + 1))
                    else:
                        ports = list(range(1, 65535))
                        ports = list(range(1, 65535))
                    
                if port_option.lower() == "-m":
                    ports = [20, 21, 22, 23, 25, 53, 80, 443, 1194, 3306, 5000, 5432, 8000, 8080, 8291, 8728, 9050]
                    
                openPorts = []
                for port in ports:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.settimeout(0.8)
                            s.settimeout(0.8)
                            result = s.connect_ex((ip, port))
                            if result == 0:
                                print(f"[+] {port} --> OPEN")
                                openPorts.append({port: 'open'})
                            s.close()

                    except socket.error as e:
                        print(f'Error: {e}')
                        return str(e)
                    except KeyboardInterrupt:
                        print('[!] Sniffer interrupted')
                        quit()
                return openPorts
            else:
                error = '[!] The options are -a for all ports and -m for main ports!'
                print(error)
                return error

        except Exception as e:
            print(f"Error: {e}")
            return str(e)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        port_option = str(sys.argv[2])
        port_option = str(sys.argv[2])
        scanner = PortScan()
        scanner.scanPorts(ip, port_option)
    elif len(sys.argv) == 5 and sys.argv[2].lower() == '-a':
        ip = sys.argv[1]
        port_option = sys.argv[2]
        start_port = int(sys.argv[3])
        end_port = int(sys.argv[4])
        scanner = PortScan()
        scanner.scanPorts(ip, port_option, start_port, end_port)
        scanner.scanPorts(ip, port_option, start_port, end_port)
    else:
        print(f"""Usage:\n
                ➜\tpython3 portScanner.py IP_Address -a (for all ports)\n
                ➜\tpython3 portScanner.py IP_Address -a start_port end_port\n
                ➜\tpython3 portScanner.py IP_Address -m (for main ports)""")