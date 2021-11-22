from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import filedialog
from sim_room_classes import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.io import wavfile
import pyroomacoustics as pra
import matplotlib.pyplot as plt
import pygame
from functions_for_sim import *
import buffer



def create_source_functional(amplitude=0, fs=0, frequency=0, time=0, phase=0, x=0, y=0, z=0, muted=0):
    _, audio = functions_for_sim.generateSinusoide(amplitude=amplitude, fs=fs, frequency=frequency,
                                                    time=time, phase=phase)
    return soundsource(audio=audio, samp_f=fs, pos_x=x, pos_y=y, pos_z=z, muted=muted)


def create_source_from_file(filename="", samp_f=0, t=0, t0=0, t1=0, x=0, y=0, z=0, muted=0):
    if t != t1-t0:
        t = t1-t0
    fs, audio = wavfile.read(filename)
    audio = functions_for_sim.time_trim(audio=audio, fs=fs, t_start=t0, t_end=t1)
    audio = functions_for_sim.resamplingAudio(audio=audio, fs=fs, newfs=samp_f)
    source = soundsource(audio=audio, samp_f=samp_f, pos_x=x, pos_y=y, pos_z=z, muted=muted)
    if source.audio.ndim > 1:
        source.change_to_oneD()
    return source



# initial sim room, sources and mics
sim_room = simulation_room(length=10000, width=10000, height=10000, sampf=16000, max_order=1, sources=[], microphones=[],
                 air_absorption=True, ray_tracing=False)

source1 = create_source_functional(amplitude=5000, fs=11000, frequency=5000, time=5, phase=0, x=5000, y=10,
                                                                                            z=10, muted=0)
source2 = create_source_from_file(filename='C:\passing-car-and-urban-ambience.wav', samp_f=16000, t=5, t0=0, t1=5, x=5000,
                                                                                 y=9990, z=10, muted=0)

#if source2.audio.ndim > 1:
 #   source2.change_to_oneD()

source1.resampleaudio(newfs=sim_room.fs)
source2.resampleaudio(newfs=sim_room.fs)

source2.make_same_sizes(secondsource=source1)

sim_room.add_source(source1)
sim_room.add_source(source2)

mic = microphone(pos_x=4090, pos_y=10, pos_z=10, muted=0)
sim_room.add_microphone(mic)

"""""
Data is a dictionary with - 'Room', 'Sources', 'Microphones', 'Simulation parameters' - keys correspond to
top level windows,, 'Material values', each of these is also a dictionary

there is also keys - 
'Array Sources' - to keep the array of current sources
'Count Sources' - count of all created sources( length of array sources )
'Active Sources' - to keep the array of active sources(muted=1)
'Count Active Sources' - count of only active sources (length of Active Sources

same keys for Microphone
'Array Microphones' - array of all microphones
'Count Microphones' - count of all mics
'Active Microphones' - array of active mics
'Count Active Microphones' - count of active mics

"""""
Data = {}

"""""
Data['Room'] is an array
 with 0th index - length property
 1 - width,  2 - Height,  3 - temperature,  4 - humadity,
5 - material values[]-is an array
6 - Walls - is an index of material from materail values[] array
7 - Floor - is an index of material from materail values[] array

"""""

Data['Material values'] = ['hard_surface', 'brickwork', 'rough_concrete',
                'ceramic_tiles', 'concrete_floor','plasterboard', 'glass_window', 'wood_1.6cm', 'audience_floor',
             'stage_floor', 'wooden_door', 'carpet_cotton', 'carpet_thin', 'curtains_velvet', 'studio_curtains',
                'chairs_wooden', 'audience_orchestra_choir', 'facing_brick', 'ceiling_plasterboard','theatre_audience',
                'anechoic']
Data['Room'] = [0]*7
Data['Room'][0] = int(sim_room.room_dim[0])
Data['Room'][1] = int(sim_room.room_dim[1])
Data['Room'][2] = int(sim_room.room_dim[2])
Data['Room'][3] = 0    # room temperature
Data['Room'][4] = 0    # room humadity
Data['Room'][5] = 20   # walls - index of material from Data[material values] array
Data['Room'][6] = 1    # floor - index of material from Data[material values] array


"""""
 Data['Simulation parameters']- is an array
 with 0th index - Fs property
 1 - Max order,  2 - 'RT60',  3 - Reference_mic,  4 - SNR , 5 -absorbtion ,  6 - Ray Tracing
 """""

Data['Simulation parameters'] = [0]*7
Data['Simulation parameters'][0] = sim_room.room.fs
Data['Simulation parameters'][1] = sim_room.room.max_order
Data['Simulation parameters'][2] = 0
Data['Simulation parameters'][3] = 0
Data['Simulation parameters'][4] = 0
Data['Simulation parameters'][5] = 1             #sim_room.room.air_absorption (1 - True,  0 - False)
Data['Simulation parameters'][6] = 0             #sim_room.room.ray_tracing(1 - True,  0 - False)

Data['Array Sources'] = sim_room.list_sources
Data['Active Sources'] = sim_room.active_sources()
Data['Count Sources'] = len(Data['Array Sources'])
Data['Count Active Sources'] = len(Data['Active Sources'])

"""""
data_buffer -  is a 3 dimensional array - ['Functional', 'Wav file'] - each of these is an array of arrays
Functional is a 2d array with -  9 x (count of sources with functional form) - sizes
Wav file is a 2d array with - 9 x (count of sources with wav file form) - sizes

Functional / form = 0
0th - amplitude of sources
1 - sampling frequency
2 - frequency
3 - time
4 - phase
5 - x coordinate
6 - y coord
7 - z coord
8 - muted(is a boolean - 0/1-active/disactive)

Wav file / form = 1
0th - audio of sources read from wav files
1 - sampling frequency
2 - t time = tend-tstart
3 - t start time
4 - t end time
5 - x coordinate
6 - y coordinate
7 - z coord
8 - muted(0/1 -active/disactive)

"""""


"""""
#initialization of buffer sources
data_buffer = [[[0 for x in range(Data['Count Sources'])] for y in range(9)] for z in range(2)]

# fill the initial 2 sources's parameters
# data_buffer[0] - is a functional source

data_buffer[0][0][0] = 5000       # amplitude of the source1
data_buffer[0][1][0] = 11000      # fs
data_buffer[0][2][0] = 5000       # frequency
data_buffer[0][3][0] = 5          # time
data_buffer[0][4][0] = 0          # phase
data_buffer[0][5][0] = 5000       # x coord
data_buffer[0][6][0] = 10         # y coord
data_buffer[0][7][0] = 10         # z coord
data_buffer[0][8][0] = 0          # muted

# data_buffer[1] - is a source given by wav file
# source2 is the second source,  but is the first of - data_buffer[1] array(is the first source given by wav file)

data_buffer[1][0][0] = 'C:\passing-car-and-urban-ambience.wav'         # filename of the source2
data_buffer[1][1][0] = 16000                                           # fs
data_buffer[1][2][0] = 5                                               # time
data_buffer[1][3][0] = 0                                               # t start
data_buffer[1][4][0] = 5                                               # t end
data_buffer[1][5][0] = 5000                                            # x coord
data_buffer[1][6][0] = 9990                                            # y coord
data_buffer[1][7][0] = 10                                              # z coord
data_buffer[1][8][0] = 0                                               # muted
"""""


"""""
Data['Sources'] is a 2d array with [6 x count_of_sources] sizes
oth - are audios of soundsource objects
1 - fs of soundsource objects
2 - x coordinates 
3 - y coord
4 - z coord
5 - muted 

these are parameters of already created soundsource objects
"""""
#initialization of buffer sources
#data_buffer = [[[None]*9]*2]*Data['Count Sources']
# fill the initial 2 sources's parameters
# first source - data_buffer[0]
# and parameters for functional form - data_buffer[0][0]

data_buffer = []
buffer_s1 = []
buffer_s2 = []
buffer_func_s1 = [0]*9
buffer_file_s1 = [""]
for i in range(8):
    buffer_file_s1.append(0)


buffer_func_s2 = [0]*9
buffer_file_s2 = [""]
for i in range(8):
    buffer_file_s2.append(0)


buffer_func_s1[0] = 5000           # amplitude of the source1 (form = 0)
buffer_func_s1[1] = 11000          # fs of source1
buffer_func_s1[2] = 5000           # frequency
buffer_func_s1[3] = 0              # phase
buffer_func_s1[4] = 5              # time
buffer_func_s1[5] = 5000           # x coord
buffer_func_s1[6] = 10             # y coord
buffer_func_s1[7] = 10             # z coord
buffer_func_s1[8] = 0              # muted

buffer_file_s1[0] = ""             # filename of the source1 (form = 1)
buffer_file_s1[1] = 0              # fs
buffer_file_s1[2] = 0              # t start
buffer_file_s1[3] = 0              # t end
buffer_file_s1[4] = 0              # time
buffer_file_s1[5] = buffer_func_s1[5]             # x coord
buffer_file_s1[6] = buffer_func_s1[6]             # y coord
buffer_file_s1[7] = buffer_func_s1[7]             # z coord
buffer_file_s1[8] = buffer_func_s1[8]             # muted

buffer_s1.append(buffer_func_s1)
buffer_s1.append(buffer_file_s1)

#initial source2 is a form of 2(by wav file)

buffer_file_s2[0] = 'C:\passing-car-and-urban-ambience.wav'             # filename of the source2 (form = 1)
buffer_file_s2[1] = 16000              # fs
buffer_file_s2[2] = 0              # t start
buffer_file_s2[3] = 5              # t end
buffer_file_s2[4] = 5              # time
buffer_file_s2[5] = 5000              # x coord
buffer_file_s2[6] = 9990              # y coord
buffer_file_s2[7] = 10             # z coord
buffer_file_s2[8] = 0              # muted

buffer_func_s2[0] = 0              # amplitude of the source2 (form = 0)
buffer_func_s2[1] = 0              # fs
buffer_func_s2[2] = 0              # frequency
buffer_func_s2[3] = 0              # time
buffer_func_s2[4] = 0              # phase
buffer_func_s2[5] = buffer_file_s2[5]              # x coord
buffer_func_s2[6] = buffer_file_s2[6]              # y coord
buffer_func_s2[7] = buffer_file_s2[7]              # z coord
buffer_func_s2[8] = buffer_file_s2[8]              # muted

buffer_s2.append(buffer_func_s2)
buffer_s2.append(buffer_file_s2)

data_buffer.append(buffer_s1)
data_buffer.append(buffer_s2)
source_forms = [0]*Data['Count Sources']
source_forms[0] = 0     # first source is functional
source_forms[1] = 1     # second is file

#initial buffer microphone
#there is one microphone
buffer_mics = []
mic_1 = [0]*4
mic_1[0] = mic.pos_x
mic_1[1] = mic.pos_y
mic_1[2] = mic.pos_z
mic_1[3] = mic.muted
buffer_mics.append(mic_1)

"""""
data_buffer[0][0][0] = 5000           # amplitude of the source1 (form = 0)
data_buffer[0][0][1] = 11000          # fs
data_buffer[0][0][2] = 5000           # frequency
data_buffer[0][0][3] = 5              # time
data_buffer[0][0][4] = 0              # phase
data_buffer[0][0][5] = 5000           # x coord
data_buffer[0][0][6] = 10             # y coord
data_buffer[0][0][7] = 10             # z coord
data_buffer[0][0][8] = 0              # muted

data_buffer[0][1][0] = ""             # filename of the source1 (form = 1)
data_buffer[0][1][1] = 0              # fs
data_buffer[0][1][2] = 0              # time
data_buffer[0][1][3] = 0              # t start
data_buffer[0][1][4] = 0              # t end
data_buffer[0][1][5] = 0              # x coord
data_buffer[0][1][6] = 0              # y coord
data_buffer[0][1][7] = 0              # z coord
data_buffer[0][1][8] = 0              # muted


# first source - data_buffer[1]
data_buffer[1][0][0] = 0              # amplitude of the source2 (form = 0)
data_buffer[1][0][1] = 0              # fs
data_buffer[1][0][2] = 0              # frequency
data_buffer[1][0][3] = 0              # time
data_buffer[1][0][4] = 0              # phase
data_buffer[1][0][5] = 0              # x coord
data_buffer[1][0][6] = 0              # y coord
data_buffer[1][0][7] = 0              # z coord
data_buffer[1][0][8] = 0              # muted

data_buffer[1][1][0] = ""             # filename of the source2 (form = 1)
data_buffer[1][1][1] = 0              # fs
data_buffer[1][1][2] = 0              # time
data_buffer[1][1][3] = 0              # t start
data_buffer[1][1][4] = 0              # t end
data_buffer[1][1][5] = 0              # x coord
data_buffer[1][1][6] = 0              # y coord
data_buffer[1][1][7] = 0              # z coord
data_buffer[1][1][8] = 0              # muted

"""""

Data['Sources'] = [[0 for x in range(6)] for y in range(Data['Count Sources'])]
for i in range(Data['Count Sources']):
    Data['Sources'][i][0] = Data['Array Sources'][i].audio
    Data['Sources'][i][1] = Data['Array Sources'][i].samp_f
    Data['Sources'][i][2] = Data['Array Sources'][i].pos_x
    Data['Sources'][i][3] = Data['Array Sources'][i].pos_y
    Data['Sources'][i][4] = Data['Array Sources'][i].pos_z
    Data['Sources'][i][5] = Data['Array Sources'][i].muted


Data['Array Microphones'] = sim_room.list_microphones
Data['Active Microphones'] = sim_room.active_mics()
Data['Count Microphones'] = len(Data['Array Microphones'])
Data['Count Active Microphones'] = len(Data['Active Microphones'])

Data['Microphones'] = [[0 for x in range(4)] for y in range(Data['Count Microphones'])]
for i in range(Data['Count Microphones']):
    Data['Microphones'][i][0] = Data['Array Microphones'][i].pos_x
    Data['Microphones'][i][1] = Data['Array Microphones'][i].pos_y
    Data['Microphones'][i][2] = Data['Array Microphones'][i].pos_z
    Data['Microphones'][i][3] = Data['Array Microphones'][i].muted
