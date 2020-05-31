''' Andrei Popa, update 5-20-2020.


      Default: single;
    Available: single, sync, clone;



'''




from tkinter import *
import pandas as pd
import numpy as np
import random
import imperfect_automata_functions
import time
import os

from tooltips import tips  # Source: https://code.sololearn.com/c5dk37BDJEeK/#py
from PIL import Image
from tkinter import ttk

data = []
data_prime = []
hd_list = []
mutants = []
mutants_prime = []

colors = imperfect_automata_functions.load_colors()


#                         Initialize interface        

wolfram_window = Tk()
wolfram_window.title("imperfect_automata")
wolfram_window.state("zoomed")
wolfram_window.configure(borderwidth=1, relief="groove", bg = "#D1F2EB")

btnExit = Button (wolfram_window, text="Exit", relief="groove", command = wolfram_window.destroy, state="normal")
btnExit.place(x=3, y=675, width=239, height=50)

frame_widgets = Frame(wolfram_window, bg="#D1F2EB", relief="groove", borderwidth=0, padx=10)
frame_widgets.place(x=2, y=150)


frame_canvas = Frame(wolfram_window, bg="#D1F2EB")
frame_canvas.place(x=250, y=2, width=1275, height=770)


canvas1 = Canvas(frame_canvas, width=1250, height=300, borderwidth=1, relief="flat", bg = "white", highlightbackground = "black", highlightthickness = 1, highlightcolor= "black")

canvas_hamming = Canvas(frame_canvas, width=1250, height=150, borderwidth=0, relief="flat", bg = "#D1F2EB")

canvas2 = Canvas(frame_canvas, width=1250, height=300, borderwidth=1, relief="flat", bg = "white", highlightbackground = "black", highlightthickness = 1, highlightcolor= "black")


print("\n")
# --------------------------------------------------------------------------  Scenarios

def scenario_sync():
    colors=imperfect_automata_functions.load_colors()
    lblScenarios.config(text="sync", bg=colors["sync"])    
    btnInitializeAutomata.config(state="normal", bg=colors["selected"])
    
    all_children = []
    all_children = frame_widgets.grid_slaves()

    for item in all_children:
        item.pack_forget()

    frame_widgets.update()

    grid_my_widgets("sync")

    frame_widgets.nametowidget("txtHeight").delete(0, END)
    frame_widgets.nametowidget("txtHeight").insert(0, 300)
    frame_widgets.nametowidget("txtWidth").delete(0, END)
    frame_widgets.nametowidget("txtWidth").insert(0, 1250)

    frame_widgets.update()
   
    y_location = frame_widgets.winfo_y() + frame_widgets.winfo_height() + 5
    frame_run.place(x=2, y=y_location, width= 240, height= 40)


    canvas1.delete("all")
    canvas1.pack(pady=2, anchor=W)
    canvas1.config(height=300, width=1250)
    canvas1.update()
    canvas1.create_text(300, 150, text=f"Automaton 1", font=(12))

    canvas_hamming.delete("all")
    canvas_hamming.pack(pady=2, anchor=W)
    canvas_hamming.config(height=150, width=1250)
    canvas_hamming.update()
    canvas_hamming.create_text(300, 75, text="Dissimilarity index (0 = identical)", font=(12))

    canvas2.delete("all")
    canvas2.pack(pady=2, anchor=W)
    canvas2.config(height=300, width=1250)
    canvas2.update()
    canvas2.create_text(300, 150, text=f"Automaton 2", font=(12))






def scenario_single():
    colors=imperfect_automata_functions.load_colors()
    lblScenarios.config(text="single", bg=colors["single"])
    btnInitializeAutomata.config(state="normal", bg=colors["selected"])

    all_children = []
    all_children = frame_widgets.grid_slaves()

    for item in all_children:
        item.grid_forget()

    frame_widgets.update()

    grid_my_widgets("single")

    frame_widgets.nametowidget("txtHeight").delete(0, END)
    frame_widgets.nametowidget("txtHeight").insert(0, 500)
    frame_widgets.nametowidget("txtWidth").delete(0, END)
    frame_widgets.nametowidget("txtWidth").insert(0, 1250)

    frame_widgets.update()

    y_location = frame_widgets.winfo_y() + frame_widgets.winfo_height() + 5
    frame_run.place(x=2, y=y_location, width= 240, height= 40)


    canvas1.delete("all")
    canvas1.pack(pady=2)
    canvas1.config(height=500, width=1250)
    canvas1.update()
    canvas1.create_text(300, 250, text="Automaton 1", font=(12))

    canvas_hamming.pack_forget()
    canvas2.pack_forget()

    







def clone_and_hide_mutants():
    colors=imperfect_automata_functions.load_colors()
    lblScenarios.config(text="clone", bg=colors["clone"])
    btnInitializeAutomata.config(state="normal", bg=colors["selected"])





frame_scenarios = Frame(wolfram_window, bg="#D1F2EB", relief="flat", borderwidth=1)
frame_scenarios.place(x=2, y=2, width = 240, height = 140)

lblScenarios = Label(frame_scenarios, text="Select a scenario to continue.", relief="flat", bg="#D1F2EB", width=27, height=2, font=("Arial", 10, "bold"))

btnSync = Button (frame_scenarios, text="Sync", relief="groove", bg=colors["sync"], command = scenario_sync, width=9, height=2)
btnSingle = Button (frame_scenarios, text="Single", relief="groove", bg=colors["single"], command = scenario_single, width=9, height=2)
btnCloneTop =  Button (frame_scenarios, relief="groove", bg=colors["clone"], command = clone_and_hide_mutants, width=9, height=2, state="disabled")

a = 3 ; b = 3  # padding

lblScenarios.grid(row=0, column=0, columnspan=27, rowspan=3, padx=a, pady=b, sticky=E+W+N+S)
btnSync.grid(row=3, column=0, columnspan=9, rowspan=3, padx=a, pady=b, sticky=N+S+E+W)
btnSingle.grid(row=3, column=9, columnspan=9, rowspan=3, padx=a, pady=b, sticky=N+S+E+W)
btnCloneTop.grid(row=3, column=18, columnspan=9, rowspan=3, padx=a, pady=b, sticky=N+S+E+W)

# ---------------------------------------------------------------------------------------------------  Parameters and their Widgets


def grid_my_widgets(scenario):
    
    widgets_dict = {}
    widgets_dict = imperfect_automata_functions.load_widgets_dict(scenario)

    row = 0
    
    for key in widgets_dict:
        if row==len(widgets_dict)/3:
            row=0
            
        val = widgets_dict[key]["val"]
        col = widgets_dict[key]["col"]
        
        if "lbl" in key:
            obj = Label(frame_widgets, name=key, text=val, anchor="e", bg=colors["widget"], width=10)
            obj.grid(column=col, row=row, padx=2, pady=2, sticky=N+S+E+W)

        elif "txt" in key:
            obj = Entry(frame_widgets, name=key, justify="center", bg=colors["widget"], width=9)
            obj.grid(column=col, row=row, padx=2, pady=2, sticky=N+S+E+W)
            obj.insert(0, val)

        else:
            obj = Label(frame_widgets, name=key, text=val, anchor="w",  bg=colors["widget"], fg = "#1a4a5c", width=9)
            obj.grid(column=col, row=row, padx=2, pady=2, sticky=N+S+E+W)

        row += 1


    for k in widgets_dict:
        if widgets_dict[k]["col"]==2:
            frame_widgets.nametowidget(k).config(fg="#1a4a5c")


    for j in widgets_dict:
        if widgets_dict[j]["single"]==0:
            frame_widgets.nametowidget(j).config(bg=colors["sync"])

    frame_widgets.update()



grid_my_widgets("single")


# ------------------------------------------------------------------------------------------------  Parameters and their Widgets
frame_run = Frame(wolfram_window, bg="#D1F2EB", relief="groove", borderwidth=0, padx=5)

y_location = frame_widgets.winfo_y() + frame_widgets.winfo_height() + 5

frame_run.place(x=2, y=y_location, width= 240, height= 40)

btnInitializeAutomata = Button (frame_run, text="Initialize", relief="groove",  state="disabled", width=1)
btnRunAutomata = Button (frame_run, text="Run", relief="groove",  state="disabled", width=1)

btnInitializeAutomata.pack(side=LEFT, fill=BOTH, expand=True, padx=2)
btnRunAutomata.pack(side=LEFT, fill=BOTH, expand=True, padx=2)


# ----------------------------------------------------------------------------  Initial conditions:

def initialize_automata():

    scn_color = lblScenarios.cget("text")
    btnRunAutomata.config(state="normal", bg=colors["selected"])

    cvs_width = int(frame_widgets.nametowidget("txtWidth").get())
    cvs_height = int(frame_widgets.nametowidget("txtHeight").get())

    canvas1.delete("all")
    canvas1.configure(width=cvs_width, height=cvs_height)
    canvas1.update()

    rule1 = int(frame_widgets.nametowidget("txtRule1").get())
    frame_widgets.nametowidget("txtRuleCode1").delete(0, END)
    frame_widgets.nametowidget("txtRuleCode1").insert(0, "{0:08b}".format(int(rule1)))

    s = int(frame_widgets.nametowidget("txtCellSize").get())
    this_gen=[]
    this_gen_mutants = []
    max_cells = int(cvs_height/s)

    this_gen = imperfect_automata_functions.random_generation(max_cells)
    padded_gen = imperfect_automata_functions.wrap_this_gen(this_gen)
    data.append(padded_gen)




    for idx in range(len(this_gen)):
        if this_gen[idx] == 1:
            canvas1.create_rectangle(s, idx*s, s + s, idx*s + s, fill=colors["one"], width=1)

        elif this_gen[idx] == 0:
            canvas1.create_rectangle(s, idx*s, s + s, idx*s + s, fill=colors["zero"], width=1)



    if scn_color == "sync":

        print("")
        print(canvas2.winfo_width())
        print(canvas2.winfo_height())
        print("")

        canvas2.delete("all")
        canvas2.configure(width=cvs_width, height=cvs_height)
        canvas2.update()            

        rule2 = int(frame_widgets.nametowidget("txtRule2").get())
        frame_widgets.nametowidget("txtRuleCode2").delete(0, END)
        frame_widgets.nametowidget("txtRuleCode2").insert(0, "{0:08b}".format(int(rule2)))        

        this_gen_prime = [element for element in this_gen]
        this_gen_prime_mutants = [element for element in this_gen_mutants]

        # Butterflies: 
        differences = int(frame_widgets.nametowidget("txtButterflies").get())

        if differences > 0:
            differences_idx = random.sample(range(0, max_cells-1), differences)

            for item in differences_idx:
                this_gen_prime[item] = abs(this_gen_prime[item] - 1)
                canvas2.create_oval(s-10, item*s-10, s+s+10, item*s+s+10, fill=colors["butterfly"], width=1)

            frame_widgets.nametowidget("txtButterflies").config(bg=colors["butterfly"])


        # Pad it and add it to the list data_prime:
        padded_gen_prime = imperfect_automata_functions.wrap_this_gen(this_gen_prime)
        data_prime.append(padded_gen_prime)

        canvas_hamming.delete("all")
        canvas_hamming.configure(width=cvs_width)
        canvas_hamming.update()


        # Hamming Distance between Canvas1 and 2:
        hd_abs, hd_percent = imperfect_automata_functions.hamming_distance(this_gen, this_gen_prime)
        hd_list.append(hd_percent)


        # 50% line
        canvas_hamming.create_line(0, canvas_hamming.winfo_height()/2, canvas_hamming.winfo_width(), canvas_hamming.winfo_height()/2, fill="gray", width=1, dash=(2,2))
        txtMidLine = Entry(canvas_hamming, fg="grey11", bg="#D1F2EB", relief="flat", font=("Helvetica", 10))
        canvas_hamming.create_window(25, canvas_hamming.winfo_height()/2-11, window=txtMidLine, height=20, width=40)
        txtMidLine.insert(0, "50%")

        # 0% and 100% limits:
        canvas_hamming.create_line(0, 10, canvas_hamming.winfo_width(), 10, fill="black", width=2, dash=(2,2))
        canvas_hamming.create_line(0, canvas_hamming.winfo_height()-10, canvas_hamming.winfo_width(), canvas_hamming.winfo_height()-10, fill="black", width=2, dash=(2,2))

        txtCanvasTitle = Entry(canvas_hamming, fg="grey11", relief="flat", bg="#D1F2EB", font=("Helvetica", 10, "bold"))  
        canvas_hamming.create_window(150, 25, window=txtCanvasTitle, height=20, width=150)
        txtCanvasTitle.insert(0, "Hamming Distance")

        canvas_hamming.create_window(300, 25, window=txtHD, height=20, width=120)
     
        # Display the Hamming Distance as it runs:
        hamming_entry = str(hd_abs) + " of " + str(len(this_gen)) + "  (" + str(hd_percent)+"%)"



    #_________________________________________________________________

    # Increment generations: 
    frame_widgets.nametowidget("txtElapsedGenerations").delete(0, END)
    frame_widgets.nametowidget("txtElapsedGenerations").insert(0, 1)




btnInitializeAutomata.config(command=initialize_automata)



#__________________________________________________________________________   RUN AUTOMATA 

def run_automata():
    

    frame_widgets.nametowidget("txtMutants1").config(bg=colors["mutant"])
    rule1 = int(frame_widgets.nametowidget("txtRule1").get())
    mutation1 = float(frame_widgets.nametowidget("txtMutation1").get())

    this_gen=[]
    this_gen_mutants = []

    s = int(frame_widgets.nametowidget("txtCellSize").get())
    all_gen = int(frame_widgets.nametowidget("txtGens").get())

    mutant_size = 7
    
    gen = 1
    columns = 1
   
    blue_line = canvas1.create_line(columns*s+s+3,   0,   columns*s+s+3,    canvas1.winfo_height(),       fill="blue", width=2)



    scn_color = lblScenarios.cget("text")

    if scn_color == "sync":

        this_gen_prime=[] ; this_row_prime_mutants = []

        frame_widgets.nametowidget("txtButterflies").config(bg=colors["widget"])
        frame_widgets.nametowidget("txtMutants2").config(bg=colors["mutant"])
        rule2 = int(frame_widgets.nametowidget("txtRule2").get())
        mutation2 = float(frame_widgets.nametowidget("txtMutation2").get())

        green_line = canvas2.create_line(columns*s+s+3,   0,   columns*s+s+3,     canvas2.winfo_height(), fill="green", width=2)
        hamming_line = canvas_hamming.create_line(columns*s+s+3,    0,      columns*s+s+3,    canvas_hamming.winfo_height(), fill="red", width=2)    
        
        txtHD = Entry(canvas_hamming, fg="red4", bg="#D1F2EB", relief="flat", font=("Helvetica", 10))
        canvas_hamming.create_window(300, 18, window=txtHD, height=20, width=120)

    while gen < all_gen:

        if columns % int(canvas1.winfo_width()/s) == 0:
            columns = 0
            # overalps when the automaton wraps around itself. No pointg fixing, will be replaced 
            # by a dynamic plot.

        # Compute and store the next generation of cell states;
        this_gen, this_gen_mutants = imperfect_automata_functions.compute_next_gen(data[-1], canvas1, rule1, mutation1)
        padded_gen = imperfect_automata_functions.wrap_this_gen(this_gen)
        data.append(padded_gen)
        mutants.append(this_gen_mutants)

        turtles1 = int(frame_widgets.nametowidget("txtMutants1").get())
        turtles1 = turtles1 + sum(this_gen_mutants)
        frame_widgets.nametowidget("txtMutants1").delete(0, END)
        frame_widgets.nametowidget("txtMutants1").insert(0, turtles1)


        for x in range(len(this_gen)):
            if this_gen_mutants[x] == 1:
                canvas1.create_oval(columns*s - mutant_size, x*s - mutant_size, columns*s + mutant_size, x*s + mutant_size, fill=colors["mutant"], width=1)                
            else:
                if this_gen[x] == 1:
                    canvas1.create_oval(columns*s, x*s, columns*s, x*s, fill=colors["one"], width=0)

                elif this_gen[x] == 0:
                    canvas1.create_oval(columns*s, x*s, columns*s, x*s, fill=colors["zero"], width=0)


        # Draw indicator line(s):
        canvas1.coords(blue_line, columns*s+s+3,   0,   columns*s+s+3,   canvas1.winfo_height())
        canvas1.update()

        
        # SECOND AUTOMATON:
        if scn_color == "sync":

            this_gen_prime, this_gen_prime_mutants = imperfect_automata_functions.compute_next_gen(data_prime[-1], canvas2, rule2, mutation2)
            padded_gen_prime = imperfect_automata_functions.wrap_this_gen(this_gen_prime)
            data_prime.append(padded_gen_prime)
            mutants_prime.append(this_gen_prime_mutants)

            turtles2 = int(frame_widgets.nametowidget("txtMutants2").get())
            turtles2 = turtles2 + sum(this_gen_prime_mutants)
            frame_widgets.nametowidget("txtMutants2").delete(0, END)
            frame_widgets.nametowidget("txtMutants2").insert(0, turtles2)
            
            for xx in range(len(this_gen_prime)):

                if this_gen_prime_mutants[xx] == 1:
                    canvas2.create_oval(columns*s-mutant_size,   xx*s-mutant_size,   columns*s+mutant_size,   xx*s+mutant_size, fill=colors["mutant"], width=1)
                    
                else:
                    if this_gen_prime[xx] == 1:
                        canvas2.create_oval(columns*s, xx*s, columns*s, xx*s, fill=colors["one"], width=0)

                    elif this_gen_prime[xx] == 0:
                        canvas2.create_oval(columns*s, xx*s, columns*s, xx*s, fill=colors["zero"], width=0)

            canvas2.coords(green_line, columns*s + s + 3, 0, columns*s + s + 3, canvas2.winfo_height())
            canvas2.update()            


            # Hamming Distance:
            hd_abs, hd_percent = imperfect_automata_functions.hamming_distance(this_gen, this_gen_prime)
            hd_list.append(hd_percent)            


            hamming_entry =  f"{hd_abs} of {len(this_gen)}  ({hd_percent}%)"
            

            txtHD.delete(0, END)
            txtHD.insert(0, hamming_entry)

            unit = (canvas_hamming.winfo_height()-20)/100

            old_y = canvas_hamming.winfo_height()-10 - int((hd_list[-2])*unit)
            new_y = canvas_hamming.winfo_height()-10 - int((hd_list[-1])*unit)

            canvas_hamming.create_line(columns*s-s/2, old_y, columns*s+s/2, new_y, fill="red", width=2)
            canvas_hamming.coords(hamming_line, columns*s + s + 3, 0, columns*s + s + 3, canvas_hamming.winfo_height())
            canvas_hamming.update() 


        # Increment generations:
        gen += 1
        columns += 1

        frame_widgets.nametowidget("txtElapsedGenerations").delete(0, END)
        frame_widgets.nametowidget("txtElapsedGenerations").insert(0, gen)
    
    #-------------------------------------------------------------------
    frame_widgets.nametowidget("txtGens").config(bg = "lime")
    frame_widgets.nametowidget("txtElapsedGenerations").config(bg = "lime")
    btnInitializeAutomata.config(state="disabled", bg=colors["widget"])
    btnRunAutomata.config(state="disabled", bg=colors["widget"])
    lblScenarios.config(bg=colors["widget"], text="ta-daaa.\nSelect a scenario to continue.")



btnRunAutomata.config(command=run_automata)

wolfram_window.mainloop()

