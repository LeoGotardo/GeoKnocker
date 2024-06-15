from portScanner import PortScanner

import customtkinter as ctk
import tkinter as tk

class View(ctk.CTk):
    def __init__(self):
        self.app = ctk.CTk()
        self.create_screen()

    def create_screen(self):
        self.app.iconbitmap(default="icons/icon.ico")
        self.app.title("Sniffer")
        
        
root = View()
root.mainloop()