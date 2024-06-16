import socket
import sys
import time


class PortScanner():     
    def enter(self, host, startPort, endPort):
        print(f"[$] Strting Xcan on {host}")
        host = print(input('Insert ip address: '))
        startPort = print(input('Insert start port: '))
        endPort = print(input('Insert end port: '))
        return [host, startPort, endPort]

    def scan(self, host, port):
        pass
    
    def scanPorts(self, host, startPort, endPort):
        open_ports = []
        for port in range(startPort, endPort):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex(host, port)
                if result == 0:
                    open_ports.append(port)
                    string = f'{port}'
                    pad = string.ljust(8)
                    print(f"[+] {pad} OPEN")
                    s.close()
            except Exception:
                return "Connection error!"
        return open_ports
        
if __name__ == '__main__':
    PortScanner.enter()
    PortScanner.scanPorts()