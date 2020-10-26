# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:17:24 2020

@author: thoma
"""

##To-do:
    # Add option to colour lines based on month of the year
    # Legend
    # Fix 'replotting' so original plot is replaced
    

import tkinter as tk
from tkinter import ttk
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import xarray as xr
import glob
from PIL import ImageTk, Image
from colour import Color


LARGE_FONT = ("Verdana", 12)
HEIGHT = 500
WIDTH = 600

#Colour gradient script for month colours
red = Color("red")
colors = list(red.range_to(Color("green"),12))

class CTDPlotApp(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.wm_title(self, "CTD Plot Client")
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        for F in (StartPage, PageOne, PageTwo, GraphPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        
        self.show_frame(StartPage)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
        
        
class StartPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#80c1ff')
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button = ttk.Button(self, text="Visit Page 1", command = lambda: controller.show_frame(PageOne))
        button.pack(pady=10, padx=10)
        button2 = ttk.Button(self, text="Visit Page 2", command = lambda: controller.show_frame(PageTwo))
        button2.pack(pady=10, padx=10)
        button3 = ttk.Button(self, text="Graph Page", command = lambda: controller.show_frame(GraphPage))
        button3.pack(pady=10, padx=10)
        
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#80c1ff')
        label = tk.Label(self, text="Page One!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button2 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
        button2.pack()
        
class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#80c1ff')
        label = tk.Label(self, text="Page Two!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button2 = ttk.Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
        button2.pack()
        
        lower_frame = tk.Frame(self, bg='#80c1ff', bd=10)
        lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')
        
        # background_image = tk.PhotoImage(file='ocean_background.png')
        # background_label = tk.Label(self, image=background_image)
        # background_label.place(relwidth=1, relheight=1)
        
class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#80c1ff')
        
        
        
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        frame = tk.Frame(self, bg='#80c1ff', bd=5)
        # frame.place(relwidth=1, relheight=0.9, anchor='n')
        frame.pack()
        
        # lower_frame = tk.Frame(self, bg='#80c1ff', bd=10)
        # lower_frame.place(relx=0.5, rely=0.25, relwidth=1, relheight=1, anchor='n')
        
        # background_image = tk.PhotoImage(file='ocean_background.png')
        # background_label = tk.Label(frame, image=background_image)
        # background_label.pack()
        
        
        
        #Create figures and subplots
        f = Figure(figsize=(8,5), dpi = 100)
        f.suptitle('Jan-June CTD Casts', fontsize=16)
        f.subplots_adjust(hspace=0.5, wspace=0.5)
        temp_plt = f.add_subplot(231)
        temp_plt.invert_yaxis()
        temp_plt.set_title("Temperature")
        f.legend("HHZ 1",loc="upper right")
        sal_plt = f.add_subplot(232)
        sal_plt.invert_yaxis()
        sal_plt.set_title("Salinity")
        dox_plt = f.add_subplot(233)
        dox_plt.invert_yaxis()
        dox_plt.set_title("DOX")
        par_plt = f.add_subplot(234)
        par_plt.invert_yaxis()
        par_plt.set_title("PAR")
        cphl_plt = f.add_subplot(235)
        cphl_plt.invert_yaxis()
        cphl_plt.set_title("Chlorophyll")
        turb_plt = f.add_subplot(236)
        turb_plt.invert_yaxis()
        turb_plt.set_title("Turbidity")
        
        # turb_plt.set_xlim(-10, 100)
        # turb_plt.set_ylim(-10, 100)
        
        
        
        selected = tk.StringVar()
        selected.set("Select")
        
        selected_mooring = ""
        
        def dropdown_func():
            print("Button clicked!", selected.get())
            
            selected_mooring = str(selected.get())
            print(selected_mooring)
            for file in glob.glob('GBROOS_CTD_NetCDF/' + selected_mooring + '/*.nc'):
                print(file)
                ds = xr.open_dataset(file)
                df = ds.to_dataframe()
                # df = df.convert_objects(convert_numeric=True)
                
                #Continue loop if missing data
                if 'PRES_REL' not in df.columns:
                    print(file + " is missing PRES_REL")
                    continue
                if 'TEMP' not in df.columns:
                    print(file + " is missing PAR")
                    continue
                if 'PSAL' not in df.columns:
                    print(file + " is missing PSAL")
                    continue
                if 'DOX' not in df.columns:
                    print(file + " is missing DOX")
                    continue
                if 'PAR' not in df.columns:
                    print(file + " is missing PAR")
                    continue
                if 'CPHL' not in df.columns:
                    print(file + " is missing CPHL")
                    continue
                # if 'TURB' not in df.columns:
                #     print(file + " is missing TURB")
                #     continue
                
                #First of second half of the year
                # if int((str(time)[23:25])) <= 6:
                #     sem = "First Half"
                # if int((str(time)[23:25])) >= 6:
                #     sem = "Second Half"
                    
                #Variables
                time = df['TIME']
                temp = df['TEMP']
                pres = df['PRES_REL']
                sal = df['PSAL']
                dox = df['DOX']
                par = df['PAR']
                cphl = df['CPHL']
                # turb = df['TURB']
                
                # Create the legend
                f.legend([temp_plt, sal_plt, dox_plt, par_plt, cphl_plt],     # The line objects
                #labels=(str(time)[18:28]),   # The labels for each line
                loc="right",   # Position of legend
                borderaxespad=1,    # Small spacing around legend box
                title="Legend Title"  # Title for the legend
                )
                # f.label=((str(time)[18:28]))
                #Plot variables
                
                temp_plt.plot(temp,pres)
                temp_plt.legend(loc="upper right")
                sal_plt.plot(sal,pres)
                dox_plt.plot(dox, pres)
                par_plt.plot(par, pres)
                cphl_plt.plot(cphl, pres)
                # turb_plt.plot(turb)
                
            #Add plot to tkinter canvas
            canvas = FigureCanvasTkAgg(f, frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
            
            toolbar = NavigationToolbar2Tk(canvas, frame)
            toolbar.update()
            # canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
            
            
        mooringList = ('YON', 'HIS', 'HIN', 'MYR', 'LSL', 'PPS')
        dropdown = tk.OptionMenu(frame, selected, *mooringList)#, command=selected)
        # dropdown.place(relwidth=0.1, relheight=0.2)
        dropdown.pack()
        
        plot_button = tk.Button(frame, text="Plot it", command=dropdown_func)
        plot_button.pack()
        #Loop through files
                    
        
        
        
        
        
        
        ##Style the window to look like the easy gui
        
app = CTDPlotApp()
app.geometry("1280x720")
app.mainloop()
    