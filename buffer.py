from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import filedialog
# from two_diff_sinusoide_sound import *
from sim_room_classes import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.io import wavfile
import pyroomacoustics as pra
import matplotlib.pyplot as plt
import pygame
from functions_for_sim import *
from sim_room_classes import *
from simulation_data import *

"""""
 previous_obj_index - what source is on window
 source_forms=[] - is an array, indexes(+1) indicate sources, and elements are 0 or 1 - indicatinf forms 
                                                            0- for functional,  and 1- for file
 data_buffer - is a 3d array with [ count_of_sources x 2 x 9 ] sizes
 sources, and each source is a 2d array, [2x9] sizes, 9 parameters for 2 forms
 so each source can have 2 form 

 array_entries - 2d array - array_entries[form=0] = [amplitude, fs, frequency, time, phase, x, y, z, muted]
                      array_entries[form=1] = [filename, fs, t, t0, t1, x, y, z, muted] entries

 """""

"""""
class BufferSources:
    def __init__(self, previous_obj_index=0, form=0, data_buffer=[], array_entries=[]):
        self.previous_obj_index = previous_obj_index
        self.form = form
        self.data_buffer = data_buffer
        self.array_entries = array_entries

    def fill_entries(self):
        if len(self.data_buffer[self.form][0]) == 0:     # if there is no source, fill all entries with default 0/""  values
            for i in range(len(self.array_entries[self.form])):        # for each entry in array_entries[form]
                if isinstance(self.array_entries[self.form][i].get(), int):
                    self.array_entries[self.form][i].insert(END, 0)    # each entry fill 0 value
                else:    # for string(filename) when form=1
                    self.array_entries[self.form][i].insert(END, "")
        else:  #if there is source, fill entries with corresponding values
            for i in range(len(self.array_entries[self.form])):
                self.array_entries[self.form][i].insert(END, self.data_buffer[self.form][i][self.previous_obj_index])

    def read_from_entries(self):
        for i in range(len(self.array_entries[self.form])):
            self.data_buffer[self.form][i][self.previous_obj_index] = int(self.array_entries[self.form][i].get())


    # for giving values from buffer to general Data in the end
    def transfer_to_general_data(self, general=[]):
        for i in range(len(self.data_buffer[self.form])):
            for j in range(len(self.data_buffer[self.form][i])):
                general[self.form][i][j] = self.data_buffer [self.form][i][j]

"""""


class BufferSources:
    def __init__(self, prev_obj_index=0, source_forms=[], data=[], entries=[]):
        self.prev_obj_index = prev_obj_index
        self.source_forms = source_forms
        self.data = data
        self.entries = entries

    # fiil previous_object's entries
    # def fill_entries(self):
    #    for i in range(9):
    #        self.entries[self.source_forms[self.prev_obj_index]][i].insert(0, self.data_buffer[self.previous_obj_ind][self.form][i])

    def fill_entries(self, s_index, s_form):
        for i in range(8):
            self.entries[s_form][i].delete(0, END)
            self.entries[s_form][i].insert(0, self.data[s_index][s_form][i])
        self.entries[s_form][8].set(self.data[s_index][s_form][8])

    def read_from_entries(self):
        form = self.source_forms[self.prev_obj_index]
        for i in range(9):
            if form == 1 and i == 0:
                self.data[self.prev_obj_index][form][i] = self.entries[form][0].get()
                continue
            self.data[self.prev_obj_index][form][i] = int(self.entries[form][i].get())
            if i >= 5:
                self.data[self.prev_obj_index][1 - form][i] = int(self.entries[form][i].get())


    def transfer_to_general_data(self, general=[]):
        for i in range(len(self.data)-len(general)):
            general.append([None]*6)
        for i in range(len(self.data)):  # each source
            form = self.source_forms[i]
            if form == 0:  # functional
                source = create_source_functional(amplitude=self.data[i][form][0],
                                                  fs=self.data[i][form][1],
                                                  frequency=self.data[i][form][2],
                                                  time=self.data[i][form][4],
                                                  phase=self.data[i][form][3],
                                                  x=self.data[i][form][5],
                                                  y=self.data[i][form][6],
                                                  z=self.data[i][form][7],
                                                  muted=self.data[i][form][8])
            else:    # with file
                source = create_source_from_file(filename=self.data[i][form][0],
                                                 samp_f=self.data[i][form][1],
                                                 t=self.data[i][form][4],
                                                 t0=self.data[i][form][2],
                                                 t1=self.data[i][form][3],
                                                 x=self.data[i][form][5],
                                                 y=self.data[i][form][6],
                                                 z=self.data[i][form][7],
                                                 muted=self.data[i][form][8])
            general[i][0] = source.audio
            general[i][1] = source.samp_f
            general[i][2] = source.pos_x
            general[i][3] = source.pos_y
            general[i][4] = source.pos_z
            general[i][5] = source.muted

class BufferMicrophones:
    def __init__(self, prev_obj_index=0, data=[], entries=[]):
        self.prev_obj_index = prev_obj_index
        self.data = data
        self.entries = entries

    def fill_entries(self):
        print(self.prev_obj_index)
        print(self.data)
        for i in range(3):
            self.entries[i].delete(0, END)
            self.entries[i].insert(0, self.data[self.prev_obj_index][i])
        self.entries[3].set(self.data[self.prev_obj_index][3])

    def read_from_entries(self):
        for i in range(4):
            self.data[self.prev_obj_index][i] = int(self.entries[i].get())

    def transfer_to_general_data(self, general=[]):
        for i in range(len(self.data)):
            for j in range(4):
                general[i][j] = self.data[i][j]














