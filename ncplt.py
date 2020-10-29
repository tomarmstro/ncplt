# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 17:17:24 2020

@author: thoma
"""

##To-do:
    # Add option to set axis bounds? Either default values or add entries for them?
    # MatplotlibDeprecationWarning error with resetting axes?
    # Add option to colour lines based on month of the year
    # Solve for the 'continue fix' of missing data
    # Solved - Fix 'replotting' so original plot is replaced
    # Solved - What's wrong with all turbidity data? Missing?
    # Solved - Legend
    
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
file_path = 'GBROOS_CTD_NetCDF/'

#Colour gradient script for month colours list
first_color = Color("blue")
second_color = Color("red")
#This color gradient works, but not with a smaller list - rgb hex's might get too specific for matplotlib?
colors_enabled = 1  #Y/N

         

colors = list(first_color.range_to(second_color,8))



#6 is red
#colors[6] is red
#label=file[46:54]


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

#Placeholder page        
class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#80c1ff')
        
        label = tk.Label(self, text="Page One!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
        button2 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
        button2.pack()

#Placeholder page         
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

#Plotting Page        
class GraphPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#80c1ff')
        
        frame = tk.Frame(self, bg='#80c1ff', bd=5)
        frame.place(relwidth=1, relheight=1)
        
        background_label = tk.Label(frame)
        background_label.pack()
        
        # lower_frame = tk.Frame(self, bg='#80c1ff', bd=10)
        # lower_frame.place(relx=0.5, rely=0.25, relwidth=1, relheight=1, anchor='n')
        
        #Background picture - if causing image errors just comment out or reload kernel to fix
        image1 = Image.open("ocean_background.png")
        image2 =  ImageTk.PhotoImage(image1)
        image_label = ttk.Label(frame, image=image2)
        background_label.image = image2
        image_label.place(relheight=1, relwidth=1)
        
        #Create figures and subplots
        f = Figure(figsize=(8,6), dpi = 100)
        f.suptitle('CTD Profiles', fontsize=16)
        f.subplots_adjust(hspace=0.5, wspace=0.5)
        
        #variables for dropdown and checkbox
        selected = tk.StringVar()
        selected.set("Select")
        check_var = tk.IntVar()
                
        #Create canvas and toolbar - outside function so toolbar is only created on startup, not button press
        canvas = FigureCanvasTkAgg(f, frame)
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        
        #plotting function, draws canvas and plots data according to selected mooring
        def dropdown_func():
            print("Button clicked!", selected.get())
            #create subplots
            temp_plt = f.add_subplot(231)
            sal_plt = f.add_subplot(232)
            dox_plt = f.add_subplot(233)
            par_plt = f.add_subplot(234)
            cphl_plt = f.add_subplot(235)
            turb_plt = f.add_subplot(236)
            
            variables_plt = [temp_plt, sal_plt, dox_plt, par_plt, cphl_plt, turb_plt]
            
            #clear any plotted data
            for var in variables_plt:
                var.cla()
            # temp_plt.cla()
            # sal_plt.cla()
            # dox_plt.cla()
            # par_plt.cla()
            # cphl_plt.cla()
            # turb_plt.cla()
            
            #invert axis and apply subplot labels
                var.invert_yaxis()
            # temp_plt.invert_yaxis()
            # sal_plt.invert_yaxis()
            # dox_plt.invert_yaxis()
            # par_plt.invert_yaxis()
            # cphl_plt.invert_yaxis()
            # turb_plt.invert_yaxis()
            
            temp_plt.set_title("Temperature")
            sal_plt.set_title("Salinity")
            dox_plt.set_title("DOX")
            par_plt.set_title("PAR")
            cphl_plt.set_title("Chlorophyll")
            turb_plt.set_title("Turbidity")
            
            selected_mooring = str(selected.get())
            print(selected_mooring)
            for file in glob.glob(file_path + selected_mooring + '/*.nc'):
                ds = xr.open_dataset(file)
                df = ds.to_dataframe()
                print(colors_enabled)
                # df = df.convert_objects(convert_numeric=True)
                
                ######THIS IS AN ISSUE - BREAKS LOOP IF MISSING DATA - NEED A WORKAROUND
                #Continue loop if missing data
                if 'PRES_REL' not in df.columns:
                    print(file + " is missing PRES_REL")
                    continue
                if 'TEMP' not in df.columns:
                    print(file + " is missing TEMP")
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
                
                #First or second half of the year
                # if int((str(time)[23:25])) <= 6:
                #     sem = "First Half"
                # if int((str(time)[23:25])) >= 6:
                #     sem = "Second Half"
                    
                #Data Variables
                time = df['TIME']
                temp = df['TEMP']
                pres = df['PRES_REL']
                sal = df['PSAL']
                dox = df['DOX']
                par = df['PAR']
                cphl = df['CPHL']
                # turb = df['TURB']
                
                #Set FV 0 or 1
                # fv = int(file[73])
                profile_date = file[46:54]
                profile_month = file[50:52]
                #Selects a color based on month - June coldest, Dec hottest with gradient inbetween
                monthly_colors = "%s" % colors[abs(6-int(profile_month))]
    
                #Check FV Value
                fv = int(file[file.index('FV') + 3])
                if fv == 1:
                    #Check for colour selection - Monthly or random?
                    #unhappy with writing this twice for two color variants. Couldn't find phrase for default colors.
                    if check_var.get() == 1:
                        temp_plt.plot(temp, pres, label=profile_date, color=monthly_colors)
                        sal_plt.plot(sal, pres, color=monthly_colors)
                        dox_plt.plot(dox, pres, color=monthly_colors)
                        par_plt.plot(par, pres, color=monthly_colors)
                        cphl_plt.plot(cphl, pres, color=monthly_colors)
                        f.legend(title="Legend", prop={'size': 7}, loc=1)
                    elif check_var.get() == 0:
                        temp_plt.plot(temp, pres, label=profile_date)
                        sal_plt.plot(sal, pres)
                        dox_plt.plot(dox, pres)
                        par_plt.plot(par, pres)
                        cphl_plt.plot(cphl, pres)
                        f.legend(title="Legend", prop={'size': 7}, loc=1)
            
            #Add plot to tkinter canvas
            canvas.draw()
            canvas.get_tk_widget().place(relwidth=0.8, relheight=0.7, relx=0.1, rely=0.2)  
        
        #add buttons, labels and dropdown menu/button
        button1 = ttk.Button(frame, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.place(relwidth=0.08, relheight=0.03, relx=0.46, rely=0.06)
        label = tk.Label(frame, text="Graph Page", font=LARGE_FONT)
        label.place(relwidth=0.12, relheight=0.03, relx=0.44, rely=0.02)
        mooringList = ('YON', 'HIS', 'HIN', 'MYR', 'LSL', 'PPS')
        dropdown = tk.OptionMenu(frame, selected, *mooringList)
        dropdown.place(relwidth=0.2, relheight=0.075, relx=0.35, rely=0.1)
        checkbox = tk.Checkbutton(frame, text='Monthly Colors', variable=check_var)
        checkbox.place(relwidth=0.15, relheight=0.04, relx=0.7, rely=0.1)
        plot_button = tk.Button(frame, text="Plot it", command=dropdown_func)
        plot_button.place(relwidth=0.05, relheight=0.075, relx=0.56, rely=0.1)
        
app = CTDPlotApp()
app.geometry("1280x720")
app.mainloop()
    
