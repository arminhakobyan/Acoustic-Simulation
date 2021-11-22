from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from two_diff_sinusoide_sound import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.io import wavfile
import pyroomacoustics as pra
import matplotlib.pyplot as plt
import pygame
from functions_for_sim import *
import pyroomacoustics
import pyroomacoustics as pra
import numpy as np
import scipy.signal
from scipy.io import wavfile
import matplotlib.pyplot as plt
import sounddevice as sd
import time
import math
import functions_for_sim
import wave
import sys
from sim_room_classes import *


# testing sound_simulation


sim_room = simulation_room(length=10000, width=10000, height=10000, sampf=16000, max_order=1, sources=[], microphones=[],
                 air_absorption=True, ray_tracing=False)

amp = 5000
fs = 11000
freq = 5000
t = 5
ph = 0

_, audio1 = functions_for_sim.generateSinusoide(amplitude=amp, fs=fs, frequency=freq, time=t, phase=ph)
source1 = soundsource(audio=audio1, samp_f=fs, pos_x=5000, pos_y=10, pos_z=10, muted=0)

fs2, audio2 = wavfile.read('C:\passing-car-and-urban-ambience.wav')
source2 = soundsource(audio=audio2, samp_f=fs2, pos_x=5000, pos_y=9990, pos_z=10, muted=0)

fs3, audio3 = wavfile.read('C:\cars-starting.wav')
source3 = soundsource(audio=audio3, samp_f=fs3, pos_x=1000, pos_y=5000, pos_z=1110, muted=0)

if source2.audio.ndim > 1:
    source2.change_to_oneD()

if source3.audio.ndim > 1:
    source3.change_to_oneD()

source1.resampleaudio(newfs=sim_room.fs)
source2.resampleaudio(newfs=sim_room.fs)
source3.resampleaudio(newfs=sim_room.fs)

source2.make_same_sizes(secondsource=source1)
source3.make_same_sizes(secondsource=source1)

sim_room.add_source(source1)
sim_room.add_source(source2)
sim_room.add_source(source3)

mic = microphone(pos_x=4090, pos_y=10, pos_z=10, muted=0)
sim_room.add_microphone(mic)

sim_room.plot_room()
sim_room.generate_image_sources()
sim_room.compute_rir()
sim_room.simulate()

sim_room.room.mic_array.to_wav("C:\Simulation results\Two_diff_waveform_sim.wav", norm=True, bitdepth=np.int16)

mic = scipy.io.wavfile.read("C:\Simulation results\Two_diff_waveform_sim.wav")
audio = mic[1]
