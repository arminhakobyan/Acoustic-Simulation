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


class soundsource:
    def __init__(self, audio, samp_f=0, pos_x=0, pos_y=0, pos_z=0, muted=0):
        self.audio = audio
        self.samp_f = samp_f
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.muted = muted

    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0

    def change_to_oneD(self):
        self.audio = functions_for_sim.twoDaudio_to_1Daudio(twod=self.audio)

    def resampleaudio(self, newfs):
        self.audio = functions_for_sim.resamplingAudio(audio=self.audio, fs=self.samp_f, newfs=newfs)

    def make_same_sizes(self, secondsource):
        self.audio, secondsource.audio = functions_for_sim.make_same_sizes(audio1=self.audio, audio2=secondsource.audio)

    def add_time_delay(self, t_from_start, t_from_end):
        self.audo = functions_for_sim.add_time_delay(t1=t_from_start, t2=t_from_end, audio=self.audio, fs=self.samp_f)

    def trim(self, t_start, t_end):
        self.audo = functions_for_sim.time_trim(audio=self.audio, fs=self.samp_f, t_start=t_start, t_end=t_end)


class microphone:
    def __init__(self, pos_x=0, pos_y=0, pos_z=0, muted=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.muted = muted

    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0


class simulation_room:
    def __init__(self, length=10000, width=10000, height=10000, sampf=16000, max_order=1, sources=[], microphones=[],
                 air_absorption=True, ray_tracing=False):
        self.room_dim = [length, width, height]
        self.fs = sampf
        self.mat = pra.make_materials(
            ceiling=("anechoic", 0.1),
            floor=("anechoic", 0.1),
            east=("anechoic", 0.15),
            west=("anechoic", 0.15),
            north=("anechoic", 0.15),
            south=("anechoic", 0.15),
        )
        self.room = pra.ShoeBox(self.room_dim, fs=self.fs,
                                max_order=max_order, materials=self.mat, air_absorption=True, ray_tracing=False)
        self.list_sources = sources
        self.list_microphones = microphones
        #self.mic_array = self.room.mic_array

    def plot_room(self):
        fig, ax = self.room.plot(mic_marker_size=30)
        ax.set_xlim([0, 10000])
        ax.set_ylim([0, 10000])
        ax.set_zlim([0, 10000])
        plt.show()

    def add_source(self, source):
        self.room.add_source([source.pos_x, source.pos_y, source.pos_z], source.audio)
        self.list_sources.append(source)

    def active_sources(self):
        active_sources = []
        for i in range(len(self.list_sources)):
            if self.list_sources[i].muted == 0:
                active_sources.append(self.list_sources[i])

        return active_sources

    def active_mics(self):
        active_mics = []
        for i in range(len(self.list_microphones)):
            if self.list_microphones[i].muted == 0:
                active_mics.append(self.list_microphones[i])

        return active_mics

    def add_microphone(self, mic):
        self.room.add_microphone([mic.pos_x, mic.pos_y, mic.pos_z])
        self.list_microphones.append(mic)

    def generate_image_sources(self):
        self.room.image_source_model()

    def compute_rt60(self):
        return self.room.measure_rt60()

    def compute_rir(self):
        self.room.compute_rir()

    def simulate(self):
        self.room.simulate()
        self.list_microphones = self.room.mic_array



"""""
class sin_soundsource:
    def __init__(self, pos_x=0, pos_y=0, pos_z=0, amplitude=0, samp_f=0, frequency=0, phase=0, muted=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.amplitude = amplitude
        self.samp_f = samp_f
        self.frequency = frequency
        self.phase = phase
        self.muted = muted

    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0


class audio_soundsource:
    def __init__(self, audio, fs=0, pos_x=0, pos_y=0, pos_z=0, muted=0):
        self.audio = audio
        self.samp_f = fs
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.muted = muted

    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0

    def change_to_oneD(self):
        self.audio = functions_for_sim.twoDaudio_to_1Daudio(twod=self.audio)

    def resampleaudio(self, newfs=0):
        new_audio = functions_for_sim.resamplingAudio(audio=self.audio, fs=self.samp_f, newfs=newfs)
        self.audio = new_audio

    def make_same_sizes(self, secondsource):
        self.audio, secondsource.audio = functions_for_sim.make_same_sizes(audio1=self.audio, audio2=secondsource.audio)

    def add_time_delay(self, t_from_start, t_from_end):
        self.audo = functions_for_sim.add_time_delay(t1=t_from_start, t2=t_from_end, audio=self.audio, fs=self.samp_f)

    def trim(self, t_start, t_end):
        self.audo = functions_for_sim.time_trim(audio=self.audio, fs=self.samp_f, t_start=t_start, t_end=t_end)


class microphone:
    def __init__(self, pos_x=0, pos_y=0, pos_z=0, muted=0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.muted = muted

    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0


class simulation_room:
    def __init__(self, length=10000, width=10000, height=10000, sampf=16000, max_order=1, sources=[], microphones=[],
                 air_absorption=True, ray_tracing=False):
        self.room_dim = [length, width, height]
        self.fs = sampf
        self.mat = pra.make_materials(
            ceiling=("anechoic", 0.1),
            floor=("anechoic", 0.1),
            east=("anechoic", 0.15),
            west=("anechoic", 0.15),
            north=("anechoic", 0.15),
            south=("anechoic", 0.15),
        )
        self.room = pra.ShoeBox(self.room_dim, fs=self.fs,
                                max_order=max_order, materials=self.mat, air_absorption=True, ray_tracing=False)
        self.list_sources = sources
        self.list_microphones = microphones
        #self.mic_array = self.room.mic_array

    def plot_room(self):
        fig, ax = self.room.plot(mic_marker_size=30)
        ax.set_xlim([0, 10000])
        ax.set_ylim([0, 10000])
        ax.set_zlim([0, 10000])
        plt.show()

    def add_sin_source(self, source):
       # source = pra.soundsource.SoundSource([pos_x, pos_y, pos_z], signal=audio)
        #source = soundsource(source_x, source_y, source_z, amplitude, samp_f, frequency, phase, muted)
        _, audio = functions_for_sim.generateSinusoide(amplitude=source.amplitude, fs=source.samp_f,
                                                       frequency=source.frequency, time=5, phase=source.phase)
        self.room.add_source([source.pos_x, source.pos_y, source.pos_z], audio)
        self.list_sources.append(source)

    def add_audio_source(self, source):
        self.room.add_source([source.pos_x, source.pos_y, source.pos_z], source.audio)
        self.list_sources.append(source)

    def active_sources(self):
        active_sources = []
        for i in range(len(self.list_sources)):
            if self.list_sources[i].muted == 0:
                active_sources.append(self.list_sources[i])

        return active_sources

    def active_mics(self):
        active_mics = []
        for i in range(len(self.list_microphones)):
            if self.list_microphones[i].muted == 0:
                active_mics.append(self.list_microphones[i])

        return active_mics

    def add_microphone(self, mic_x, mic_y, mic_z, muted):
        mic = microphone(mic_x, mic_y, mic_z, muted)
        self.room.add_microphone([mic_x, mic_y, mic_z])
        self.list_microphones.append(mic)

    def generate_image_sources(self):
        self.room.image_source_model()

    def compute_rt60(self):
        return self.room.measure_rt60()

    def compute_rir(self):
        self.room.compute_rir()

    def simulate(self):
        self.room.simulate()
        self.list_microphones = self.room.mic_array

"""""


