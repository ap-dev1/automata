from tkinter import *
import pandas as pd 
import random
import os



def automaton_to_df(data_list, mutant_list):
    '''
    data_list:     the states of all cells, essentially list of lists of 1s and 0s.
    mutant_list:   same shape as the data_list; 1 = mutant, 0 = not mutant.

    Creates (and returns) two data frames:
        - my_df: the automaton, with columns labeled cell_1, cell_2, etc.
                       and generations of states as rows (rows = generations).
        - my_df_mutants: same shape as my_df; 1 = mutant, 0 = not mutant
    '''

    # create labels:
    col_labels = ["last_value"]  # row_padded
    col_labels_mutants = []      # not padded
    j=1

    while j < len(data_list[0])-1:
        my_label = "cell_" + str(j)
        col_labels.append(my_label)
        col_labels_mutants.append(my_label)
        j += 1
    
    col_labels.append("first_value")
    
    # create automaton DataFrame:
    my_df = pd.DataFrame(data_list, columns=col_labels)

    # create mutants DataFrame:
    my_df_mutants = pd.DataFrame(mutant_list, columns=col_labels_mutants)

    return my_df, my_df_mutants

    
    

def hamming_distance(list1, list2):
    
    '''Takes two lists of binary values and the desired number of bits (their length). 
    Returns the Hamming Distance between the two lists, in percentages.'''
    
    #string_length = "{0:0" + bits + "b}"
    #binary1 = string_length.format(int1)
    #binary2 = string_length.format(int2)
    
    hd=0 ; i=0

    while i < len(list1):
        if list1[i] != list2[i]:
            hd += 1        
        i += 1

    # integer between 0 and 100, to draw it on canvas 
    hd_percent = int((hd/len(list1))*100)

    return hd, hd_percent



def draw_without_mutants(my_row, my_canvas, size, columns):
    ''' 
    Clones the automaton associated with the top canvas on the bottom canvas, without drawing 
    the mutants. It's useful when the mutation rate is high and the mutants obscure the pattern.
    
    Takes this_row (PADDED) and a canvas. Returns nothing. 
    '''

    s = size
    cols = columns

    m = 0

    while m < len(my_row): 
        my_cell = my_row[m]

        if my_cell == 1:
            my_canvas.create_rectangle(cols*s, m*s, cols*s + s, m*s + s, fill="#2b2222", width=0) 

        elif my_cell == 0:
            my_canvas.create_rectangle(cols*s, m*s, cols*s + s, m*s + s, fill="white", width=0)

        m = m + 1

    # canvas2.update()
    # my_canvas.update()
#__________________________________________________________________________   end of function:   draw_without_mutants

def random_generation(nr_cells):
    random_gen = []

    for i in range(nr_cells):
        random_decimal = random.random()

        if random_decimal > 0.5:
            random_gen.append(1)
        else:
            random_gen.append(0) 

    return random_gen



def wrap_this_gen(gen1):
    '''
    Takes a list of 1s and 0s. Returns a "padded" list, with two more elements: 
            1) a copy of the first value, added to the end;
            2) a copy of the last value, added at the beginning of the list. 
    This makes it easier to wrap the automaton around itself as it evolves. 
    '''
    gen2 = [gen1[-1]]
    gen2 = gen2 + gen1
    gen2.append(gen1[0])

    return gen2


def mutation_triangle(coord_X, coord_Y):
    '''Computes the other two corners and returns the six coordinates.'''

    
    offset = 10
    length = 50
    wing = 16

    X = coord_X - offset
    Y = coord_Y
    X0, X1 = X - length, X - length
    Y0 = coord_Y - wing
    Y1 = coord_Y + wing


    return X0, Y0, X, Y, X1, Y1



def load_colors():
    my_colors = {}
    # colors
        
    my_colors = {"one":"#022241", "zero":"#DADEE2", "mutant":"#ff8000", 
    "triangle": "#011D37", "triangle_side":"#022241", "butterfly": "cyan",
    "disabled": "#1A4A5C",
    "available": "#FFA535", 
    "sync": "#85cf91", "single": "#fffcb8", "clone":"#ffd9b8",
    "highlight": "cyan", 
    "widget": "#D1F2EB", 
    "selected":"#FFA535"}


    # 85cf91 - a nice green, light
    # FFE755 - yellow-ish
    # 9FCCCA, my color, light tone
    # DADEE2, my color, lighter
    # F9FAFA  white-bluish
    # FFA535  orange-ish
    # 022D41   like mine, slighly lighter, for ones
    # 022D41   like mine, close to black
    # D34E36   orange mat
    # 363636   dark grey
    # CFCFCF   light grey 
    # BABABA   grey, so-so

    return my_colors





def get_label_names():
    my_labels = ["Width:", "Height:", "Cell size:", "Butterflies:", "Rule 1:", "Rule 2:", "Mutation 1:", "Mutation 2:", "Repetitions:", "Generations:"]

    my_right_labels = ["px", "px", "px", "cells", "txtRuleCode1", "txtRuleCode2", "txtMutants1", "txtMutants2", "txtElapsedReps", "txtAllGen"]

    return my_labels, my_right_labels



def load_widgets_dict(scenario_name):
    m1 = "0.00001"
    m2 = "0.0"
    reps = 2000
    rule1 = 110
    rule2 = 110
    code1 = "{0:08b}".format(int(rule1))
    code2 = "{0:08b}".format(int(rule2))

    first = 0 
    middle = 1
    last = 2

    my_widgets = {
    "lblWidth": {"val": "Width:", "col": first, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1},
    "lblHeight": {"val": "Height:", "col": first, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1},
    "lblCellSize": {"val": "Cell size:", "col": first, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1},
    
    "lblButterflies": {"val": "Butterflies:", "col": first, "sync": 1, "single": 0, "stack": 0, "clone": 0, "common": 0},
    "lblRule1": {"val": "Rule 1:", "col": first, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1},
    "lblRule2": {"val": "Rule 2:", "col": first, "sync": 1, "single": 0, "stack": 0, "clone": 0, "common": 0},
    "lblMutation1": {"val": "Mutation 1:", "col": first, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1},
    "lblMutation2": {"val": "Mutation 2:", "col": first, "sync": 1, "single": 0, "stack": 0, "clone": 0, "common": 0},
    "lblGens": {"val": "Generations:", "col": first, "sync": 1, "single": 1, "stack": 1, "clone": 1},

    "txtWidth": {"val": 1250, "col": middle, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1},
    "txtHeight": {"val": 300, "col": middle, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1},
    "txtCellSize": {"val": 1, "col": middle, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1}, 
    
    "txtButterflies": {"val": 1, "col": middle, "sync": 1, "single": 0, "stack": 0, "clone": 0, "common": 0},
    "txtRule1": {"val": rule1, "col": middle, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1}, 
    "txtRule2": {"val": rule2, "col": middle, "sync": 1, "single": 0, "stack": 0, "clone": 0, "common": 0},
    "txtMutation1": {"val": m1, "col": middle, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1}, 
    "txtMutation2": {"val": m2, "col": middle, "sync": 1, "single": 0, "stack": 0, "clone": 0, "common": 0},
    "txtGens": {"val": reps, "col": middle, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1}, 

    "pixels1": {"val": "pixels", "col": last, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1},
    "pixels2": {"val": "pixels", "col": last, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1},
    "pixels3": {"val": "pixels", "col": last, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1}, 
    
    "butterflies": {"val": "cell(s)", "col": last, "sync": 1, "single": 0, "stack": 0, "clone": 0, "common": 0},
    "txtRuleCode1": {"val": code1, "col": last, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1}, 
    "txtRuleCode2": {"val": code2, "col": last, "sync": 1, "single": 0, "stack": 0, "clone": 0, "common": 0},
    "txtMutants1": {"val": 0, "col": last, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1}, 
    "txtMutants2": {"val": 0, "col": last, "sync": 1, "single": 0, "stack": 0, "clone": 0, "common": 0},
    "txtElapsedGenerations": {"val": 0, "col": last, "sync": 1, "single": 1, "stack": 1, "clone": 1, "common": 1}, 
    }
    

    grid_dict = {}

    for item in my_widgets:
        scn = my_widgets[item][scenario_name]

        if scn == 1:
            grid_dict.update({item: my_widgets[item]})

    return grid_dict



def compute_next_gen(previous_row, my_canvas, rule_number, mutation_rate):

    '''
    Called by run_automata().
    Takes:
        --> previous_row:   the last generation of cell states (PADDED!), from which it will create a new generation
        --> my_canvas:      top or bottom; to know where to draw the new generation; 
        --> rule_code:      the automaton, 110 in my default; 
        --> mutation_rate:  the probability to break the rule, associated with the automaton running on my_canvas.
    
        Gets the rule number and converts it into an eigh-bit string (wolfram code).
        Uses the code to compute the next generation of cell states.
        Mutates whatever needs mutated.
    
    Returns: new_row (based on rule) and a list of mutants (their indexes).
    '''
    rule_code = "{0:08b}".format(int(rule_number))

    new_row = []
    list_of_mutants = []
    i = 1

    # Go cell by cell and bit by bit:
    while i < len(previous_row)-1: 

        if previous_row[i-1] == 1 and previous_row[i] == 1 and previous_row[i+1] == 1:
            cell_state = int(rule_code[0])
        
        elif previous_row[i-1] == 1 and previous_row[i] == 1 and previous_row[i+1] == 0:
            cell_state = int(rule_code[1])
        
        elif previous_row[i-1] == 1 and previous_row[i] == 0 and previous_row[i+1] == 1:
            cell_state = int(rule_code[2])

        elif previous_row[i-1] == 1 and previous_row[i] == 0 and previous_row[i+1] == 0:
            cell_state = int(rule_code[3])
            
        elif previous_row[i-1] == 0 and previous_row[i] == 1 and previous_row[i+1] == 1:
            cell_state = int(rule_code[4])

        elif previous_row[i-1] == 0 and previous_row[i] == 1 and previous_row[i+1] == 0:
            cell_state = int(rule_code[5])

        elif previous_row[i-1] == 0 and previous_row[i] == 0 and previous_row[i+1] == 1:
            cell_state = int(rule_code[6])

        elif previous_row[i-1] == 0 and previous_row[i] == 0 and previous_row[i+1] == 0:
            cell_state = int(rule_code[7])
        
        #  mutate cell
        rand_dec = random.random()
        
        if rand_dec < mutation_rate:
            cell_state = abs(cell_state-1)
            list_of_mutants.append(1)

        elif rand_dec >= mutation_rate:
            cell_state = cell_state
            list_of_mutants.append(0)

        new_row.append(cell_state)
        i = i + 1

    return new_row, list_of_mutants
#__________________________________________________________________________   end of function





def load_tooltips():
    my_tooltips = {}
    
    # Load from a json file. In progress.

    # tt_width = tips(txtWidth, text="canvas length, or width, in pixels; the automata evolve from left to right", bg="grey97")

    # tt_height = tips(txtHeight, text="canvas height, in px; when saving data, these cells become columns and the generations become rows.", bg="grey97")
    
    # tt_cell_size = tips(txtCellSize, text="1 is great for visualizing patterns;  50 is large, good to illustrate the concept.", bg="grey97")

    # tt_butterflies = tips(txtButterflies, text="1 = canvas1 and canvas2 start with identical initial conditions, except for one cell (chosen at random); set mutation rates to zero to see how minor differences cause the patterns to diverge with time.", bg="grey97")

    # tt_rule = tips(txtRule1, text="A number from 0 to 255 that describes an Elementary Cellular Automaton.\nLink to wolfram world", bg="grey97")

    # tt_rule = tips(txtRule2, text="A number from 0 to 255 that describes an Elementary Cellular Automaton.\nLink to wolfram world", bg="grey97")

    # tt_mutation = tips(txtMutation1, text="Probability to make a mistake when writing a new cell: put 1 instead of 0 or viceversa; equal for all cells.", bg="grey97")

    # tt_nr_mutants = tips(txtMutants1, text="nr. of mutants (canvas1 + canvas2).", bg="grey97")

    # tt_mutation2 = tips(txtMutation2, text="Mutation rate for the second automata, if applicable. Ignored if cloning is checked.", bg="grey97")

    # tt_nr_mutants = tips(txtMutants2, text="in progress.", bg="grey97")

    # tt_reps = tips(txtReps, text="1 repetition = 1 screen length; runs until the end of the screen;\nif > 1, loops back and overrides the pattern.", bg="grey97")

    # tt_btnInitialize = tips(btnInitializeAutomata, text="Initializes the automata and sets the first generation of cell states, i.e., initial conditions.", bg="grey97")

    # tt_btnLoadSaved = tips(btnLoadSaved, text="Coming soon. \nLoads saved data and plots specified ranges;", bg="grey97")
    #tt_c1 = tips(canvas1, text="Canvas1 (top).", bg="grey97")

    #tt_Hamming = tips(canvas_hamming, text="The Hamming Distance (HD) between 0110 and 1001 is four bits bit= the number of differences between two binary strings of equal length. Computes and displays the HD between the two canvases in real time, as percentages; saved in the same .xlsx file as the data.", bg="grey97")

    #tt_c2 = tips(canvas2, text="Canvas2 (bottom).", bg="grey97")

    # tt_scenario = tips(cbxScenario, text="sync: two running in parallel; \n stacked: wraps the next screen underneath; \ndatasets: coming soon", bg="grey97")

    # tt_btnInitScenario = tips(btnInitScenario, text="Each scenario has unique constraints. the automata and sets the first generation of cell states, i.e., initial conditions.", bg="grey97")

    # tt_clone = tips(cbxCloneCanvas, text="If checked, canvas2 (bottom) mirrors canvas1 (top), but without drawing the mutants. Useful when the rate of mutation is very large and mutants obscure the pattern.", bg="grey97")

    # tt_save_fig = tips(cbxSaveData, text="If checked, saves results as .csv files.\nFin progress", bg="grey97")

    # #tt_btnRunAutomata = tips(btnRunAutomata, text="Runs the automata and saves the results.\nMaThe automata must be initialized.", bg="grey97")

    # 
    # 
    # 

    return my_tooltips
