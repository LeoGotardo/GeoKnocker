import socket

from datetime import datetime

class PortScanner():
    def __init__(self, initial_port, final_port, host):
        self.initial_port = initial_port
        self.final_port = final_port
        self.host = host
        self.open_ports = []
        self.closed_ports = []
        self.scanned_ports = []