from tkinter import messagebox as msg
from GeoKnocker import PortScan
from PIL import Image as img
from custonThread import CustomThread
from CTkTable import *
from icecream import ic

import tkintermapview as tkmap
import customtkinter as ctk
import tkinter as tk


class View(ctk.CTk):
    def __init__(self):
        self.app = ctk.CTk()
        self.scanner = PortScan() 
        
        self.title = ['Port', 'Status']
        
        self.white = ctk.CTkImage(dark_image=img.open("icons/White.ico"))
        self.dark = ctk.CTkImage(dark_image=img.open("icons/Dark.ico"))

        ctk.set_appearance_mode('dark')
        
        self.host = tk.StringVar()
        self.initialPort = tk.StringVar()
        self.finalPort = tk.StringVar()
        self.switchVar = tk.StringVar(value="-m")
        
        self.thread = None
        
        self.priColor = "#1f1f1f"
        self.secColor = "#171717"
        
        self.app.iconbitmap(default="icons/icon.ico")
        self.app.title("Sniffer")
        self.app.geometry("400x500")
        self.app.resizable(False, False)
        self.mode = 'dark'
        
        self.app.protocol("WM_DELETE_WINDOW", self.askClose)
        
        self.scanScreen()
        self.app.mainloop()
        
    def theme(self, button):
        if self.mode == 'dark':
            ctk.set_appearance_mode('light')
            button.configure(image=self.dark)
            self.priColor = "#FFFFFF"
            self.secColor = "#ECECEC"
            self.mode = 'light'
        else:
            ctk.set_appearance_mode('dark')
            self.priColor = "#1f1f1f"
            self.secColor = "#171717"
            button.configure(image=self.white)
            self.mode = 'dark'

    def askClose(self): 
        response = msg.askyesno(title="Exit?", message="Are you sure you want to exit?")
        if response:
            if self.thread is not None and self.thread.is_alive():
                self.thread.raise_exception()
            self.app.destroy()

    def scan(self):
        host = self.host.get()
        initialPort = self.initialPort.get()
        finalPort = self.finalPort.get()
        port_mode = self.switchVar.get()
        
        if port_mode == '-a':
            try:
                initialPort = int(initialPort)
                finalPort = int(finalPort)
            except ValueError:
                msg.showerror(title="Error", message="Please enter valid numbers.")
                return
            
            if initialPort == 0 or finalPort == 0 or initialPort > finalPort or initialPort < 1 or finalPort > 65535:
                msg.showerror(title="Error", message="Please enter a valid port range.")
                return

        kwargs = {'ip': host, 'port_option': port_mode, 'geo': '-g'}
        if port_mode == '-a':
            if initialPort != '' and finalPort != '':  
                kwargs['rangePorts'] = [initialPort, finalPort]

        
        self.thread = CustomThread(target=self.scanner.scanPorts, args=(kwargs,))
        
        if not host:
            msg.showerror(title="Error", message="Please fill host field.")
            return
        
        self.thread.start()
        self.frame.destroy()
        self.loading()
        self.app.after(200, self.isalive)
        
    def isalive(self):
        if self.thread.is_alive():
            self.app.after(200, self.isalive)
        else:
            result = self.thread.join()

            if result is not None:
                self.open_ports, self.geo = result
            
                if isinstance(self.geo, str):
                    self.geo = {'lat': '-15.2480952', 'lon': '-124.1015625', 'city': 'No Location', 'country': 'Unknown'}
                    self.loadingComplete()
                    self.showPorts()
                    return
                
                if not self.open_ports:
                    msg.showerror(title="Error", message="No ports opened.")
                    self.loadingComplete()
                    self.scanScreen()
                    return
            
                if isinstance(self.open_ports, str):
                    msg.showerror(title="Error", message=self.open_ports)
                    self.loadingComplete()
                    self.scanScreen()
                    return
            
                self.open_ports.insert(0, self.title)
                self.loadingComplete()
                self.showPorts()
    
    
    def loadingComplete(self):
        self.loadingbar.stop()
        self.loadingFrame.destroy()
    
    
    def loading(self):
        self.loadingFrame = ctk.CTkFrame(master=self.app)
        self.app.title("Loading...")
        self.loadingFrame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            master=self.loadingFrame, 
            text="Loading...",
            font=ctk.CTkFont(family="Helvetica", size=36, weight="bold", slant="italic")
        )
        
        wait = ctk.CTkLabel(
            master=self.loadingFrame,
            text='Please wait',
            font=ctk.CTkFont(family="Helvetica", size=16)
        )

        self.loadingbar = ctk.CTkProgressBar(master=self.loadingFrame, mode='indeterminate', progress_color=self.priColor)
        self.loadingbar.start()

        title.pack(padx=100, pady=5)
        wait.pack(padx=50, pady=0)
        self.loadingbar.pack(padx=50, pady=10)

    def scanScreen(self):
        self.app.geometry("400x500")
        self.frame = ctk.CTkFrame(master=self.app, width=400, height=500)
        self.frame.pack(fill="both", expand=True)

        title = ctk.CTkLabel(
            self.frame,
            text="Sniffer",
            font=("Helvetica", 40, "italic"),
        )
        
        hostText = ctk.CTkLabel(
            self.frame,
            text="Host:",
            font=("RobotoSlab", 12),
            anchor="center",
            height=10,
            width=10,
        )
        
        hostEntry = ctk.CTkEntry(
            self.frame,
            placeholder_text='Host',
            width=200,
            textvariable=self.host,
            font=("RobotoSlab", 12),
            border_width=2,
            height=40,
            border_color=self.priColor,
        )
        
        inicialPortText = ctk.CTkLabel(
            self.frame,
            text="Initial Port (1-65535):",
            font=("RobotoSlab", 12),
            anchor="center",
            height=10,
            width=10,
        )
        
        initialPortEntry = ctk.CTkEntry(
            self.frame,
            placeholder_text='Initial Port (1-65535)',
            width=200,
            textvariable=self.initialPort,
            font=("RobotoSlab", 12),
            height=40,
            border_color=self.priColor,
        )
        
        finalPortText = ctk.CTkLabel(
            self.frame,
            text="Final Port (1-65535):",
            font=("RobotoSlab", 12),
            anchor="center",
            height=10,
            width=10,
        )
        
        finalPortEntry = ctk.CTkEntry(
            self.frame,
            placeholder_text='Final Port (1-65535)',
            width=200,
            textvariable=self.finalPort,
            font=("RobotoSlab", 12),
            height=40,
            border_color=self.priColor,
        )
        
        config = ctk.CTkSwitch(
            master=self.frame,
            text="Only main ports",
            variable=self.switchVar,
            fg_color=self.priColor,
            onvalue="-m",
            offvalue="-a",
            font=("RobotoSlab", 12),
            corner_radius=20,
            height=40,
            width=100
        )
        
        scanbtn = ctk.CTkButton(
            master=self.frame,
            text="Scan",
            command=lambda:self.scan(),
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )
        
        changeTheme = ctk.CTkButton(
            master=self.frame,
            text="",
            command=lambda:self.theme(changeTheme),
            font=("RobotoSlab", 12),
            corner_radius=50,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=10,
            width=10,
            image=self.white
        )
        
        title.place(relx=0.5, rely=0.1, anchor="center")
        hostText.place(relx=0.25, rely=0.19, anchor="w")
        hostEntry.place(relx=0.5, rely=0.25, anchor="center")
        inicialPortText.place(relx=0.25, rely=0.34, anchor="w")
        initialPortEntry.place(relx=0.5, rely=0.4, anchor="center")
        finalPortText.place(relx=0.25, rely=0.49, anchor="w")
        finalPortEntry.place(relx=0.5, rely=0.55, anchor="center")
        config.place(relx=0.5, rely=0.65, anchor="center")
        scanbtn.place(relx=0.5, rely=0.75, anchor="center")
        changeTheme.place(relx=0.5, rely=0.95, anchor="center")
        
        self.app.bind("<Return>", lambda event: self.scan())
    
    def showPorts(self):
        self.frame.destroy()
        self.app.geometry("900x600")
        self.frame = ctk.CTkFrame(master=self.app, width=400, height=500)
        self.frame.pack(fill="both", expand=True)
        
        title = ctk.CTkLabel(
            self.frame,
            text="Ports Opened",
            font=("Helvetica", 40, "italic"),
        )
        
        tableFixFrame = ctk.CTkScrollableFrame(
            master=self.frame,
            width=250,
            height=400)
        
        tableFrame = ctk.CTkFrame(
            master=tableFixFrame,
            height=10000)
        
        table = CTkTable(
            master=tableFrame,
            row=len(self.open_ports),
            column=2,
            values=self.open_ports,
            width=125,
            colors=[self.priColor, self.secColor]
        )
        
        map = tkmap.TkinterMapView(
            self.frame,
            width=500,
            height=400,
            corner_radius=20,
        )
        
        print(self.geo)
        map.set_position(float(self.geo['lat']), float(self.geo['lon']), marker=True, text='{}, {}'.format(self.geo['city'], self.geo['country']))
        map.set_zoom(15)
        
        back = ctk.CTkButton(
            master=self.frame,
            text="New Scan",
            command=lambda:[self.frame.destroy(), self.scanScreen()],
            font=("RobotoSlab", 12),
            corner_radius=20,
            fg_color=self.priColor,
            hover_color=self.secColor,
            height=40,
            width=100
        )
        
        title.place(relx=0.5, rely=0.1, anchor="center")
        tableFixFrame.place(relx=0.2, rely=0.18, anchor="n")
        tableFrame.pack(fill='both', expand=True)
        table.place(in_=tableFrame)
        map.place(relx=0.68, rely=0.18, anchor="n")
        back.place(relx=0.5, rely=0.95, anchor="center")
        
        self.app.bind("<Return>", lambda event: [self.frame.destroy(), self.scanScreen()])
        
if __name__ == "__main__":
    app = View()
