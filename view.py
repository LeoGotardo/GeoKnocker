from tkinter import messagebox as msg
from portScanner import PortScanner
from PIL import Image as img
from threading import Thread
from CTkTable import *

import customtkinter as ctk
import tkinter as tk


class CustomThread(Thread):
    """
    Initialize CustomThread Object
    
    Args:
        group(object): Thread Group.
        target(callabe): Target Function to call when thread starts.
        name(str): Thread name.
        args(tuple): arguments to pass to the target function
        kwargs(dict): keyword arguments to pass to the target function.
        verbose(bool): Verbosity level.
        
    Returns:
        The return value of the target function if it exists.
    """
    def __init__(self, group=None, target= None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None


    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


class View(ctk.CTk):
    def __init__(self):
        self.app = ctk.CTk()
        self.scanner = PortScanner() 
        
        self.white = ctk.CTkImage(dark_image=img.open("icons/White.ico"))
        self.dark = ctk.CTkImage(dark_image=img.open("icons/Dark.ico"))
        
        self.host = tk.StringVar()
        self.initialPort = tk.StringVar()
        self.finalPort = tk.StringVar()
        
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
        """
        Toggles between dark and light themes.

        Args:
            self: The instance of the class.
            button (Tkinter.Button): Button widget used to toggle the theme.

        Functionality:
            - Checks the current theme mode.
            - If the current mode is 'dark':
                - Sets the appearance mode to 'light'.
                - Changes the button image to indicate the light theme.
                - Updates the mode attribute to 'light'.
        - If the current mode is 'light':
                - Sets the appearance mode to 'dark'.
                - Changes the button image to indicate the dark theme.
                - Updates the mode attribute to 'dark'.
        """
        if self.mode == 'dark':
            ctk.set_appearance_mode('light')
            button.configure(image=self.dark)
            self.mode = 'light'
        else:
            ctk.set_appearance_mode('dark')
            button.configure(image=self.white)
            self.mode = 'dark'

    def askClose(self): 
        """
        Prompts the user to confirm the application's exit.

        Args:
            self: The instance of the class.

        Functionality:
            - Prompts the user to confirm the application's exit.
            - If the user confirms the exit, the application is closed.
            - If the user cancels the exit, the application remains open.
        """
        response = msg.askyesno(title="Exit?", message="Are you sure you want to exit?")
        if response == True:
            self.app.destroy()
        else:
            pass


    def scan(self):
        host = self.host.get()
        initialPort = self.initialPort.get()
        finalPort = self.finalPort.get()
        
        title = ['Port', 'Status']
        
        if initialPort == '' or finalPort == '' or host == '':
            msg.showerror(title="Error", message="Please fill in all fields.")
            return
        
        try:
            initialPort = int(initialPort)
            finalPort = int(finalPort)
        except ValueError:
            msg.showerror(title="Error", message="Please enter valid numbers.")
            return
        
        self.frame.destroy()
        self.loading()
           
        thread = CustomThread(target=self.scanner.scanPorts, args=(host, initialPort, finalPort))
        thread.start()
        
        self.open_ports = thread.join()
        
        if self.open_ports == []:
            msg.showerror(title="Error", message="No ports opened.")
            self.loadingComplete()
            self.scanScreen()
            return
        
        if self.open_ports == "Connection error!":
            msg.showerror(title="Error", message="Connection Error!")
            self.loadingComplete()
            self.scanScreen()
            return
        
        self.open_ports.insert(0, title)
        print(self.open_ports)
        self.loadingComplete()
        self.showPorts()
        
    
    def loadingComplete(self):
        self.loadingbar.stop()
        self.loadingFrame.destroy()
        print('loading complete')
    
    
    def loading(self):
        """
        Sets up the loading page for displaying a loading animation.

        Args:
            self: The instance of the class.

        Functionality:
            - Creates and configures the loading frame.
            - Sets the title for the application window.
            - Creates a loading animation using the tkinter.Animation module.
            - Creates a button for exiting the application.
            - Binds the Return key to trigger the exit method when pressed.
            - Places all widgets within the loading frame with appropriate configurations.
        """
        print('loading')
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
        
        title.place(relx=0.5, rely=0.1, anchor="center")
        hostText.place(relx=0.25, rely=0.24, anchor="w")
        hostEntry.place(relx=0.5, rely=0.3, anchor="center")
        inicialPortText.place(relx=0.25, rely=0.44, anchor="w")
        initialPortEntry.place(relx=0.5, rely=0.5, anchor="center")
        finalPortText.place(relx=0.25, rely=0.64, anchor="w")
        finalPortEntry.place(relx=0.5, rely=0.7, anchor="center")
        scanbtn.place(relx=0.5, rely=0.8, anchor="center")
        changeTheme.place(relx=0.5, rely=0.95, anchor="center")
        
        self.app.bind("<Return>", lambda event: self.scan())
        
    
    def showPorts(self):
        self.frame.destroy()
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
            height=300)
        
        tableFrame = ctk.CTkFrame(
            master=tableFixFrame,
            height=10000)
        
        table = CTkTable(
            master=tableFrame,
            row=len(self.open_ports),
            column=2,
            values=self.open_ports,
            width=200,
            colors=[self.priColor,'#292b29']
        )
        
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
        tableFixFrame.place(relx=0.5, rely=0.2, anchor="n")
        tableFrame.pack(fill='both', expand=True)
        table.place(in_=tableFrame)
        back.place(relx=0.5, rely=0.95, anchor="center")
        
        self.app.bind("<Return>", lambda event: [self.frame.destroy(), self.scanScreen()])
        
if __name__ == "__main__":
    app = View()