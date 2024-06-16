import socket
import sys
import time

def scan(ip, port_range):
    ports = [i for i in range(1,65535)]
    main_ports = [21, 22, 80, 443, 3306, 5000, 8000, 8080, 8291, 8728, 9050]
    avaliable = {'-m': main_ports, '-p': ports}
    if port_range in avaliable:
        for port in avaliable.get(port_range):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                s.connect((ip, port))
                resp = s.recv(1024)
                if resp:
                    print(f"[+] {port} - OPEN\n$➜\t{resp.decode()}\n\n")
            except socket.error:
                pass

            except KeyboardInterrupt:
                print('[!] Interrupted\n')
                quit()
    else:
        print('[!] The options are -p for single port and -m for main ports!')
    return ip, port_range

if __name__ == '__main__':
    if len(sys.argv) == 3:
        ip = sys.argv[1]
        port_range = sys.argv[2]
        scan(ip, port_range)
    else:
        print(f'Usage:\n➜\tpython3 portScanner.py IP_Address -a (for all ports)\n➜\tpython3 portScanner.py IP_Address -m (for main ports)')