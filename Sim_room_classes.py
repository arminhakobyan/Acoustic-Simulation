from yamlable import yaml_info, YamlAble
import pyroomacoustics as pra
import yaml
from yaml import FullLoader
from scipy.io import wavfile
import matplotlib.pyplot as plt
import Funcs_used_in_sim
import wave
import sys
import ruamel.yaml
from io import StringIO
from pathlib import Path


class soundsource():
    def __init__(self, audio=[], fs=0, x=0, y=0, z=0, muted=0):
        self.audio = audio
        self.fs = fs
        self.x = x
        self.y = y
        self.z = z
        self.muted = muted


    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0

    def change_to_oneD(self):
        self.audio = Funcs_used_in_sim.twoDaudio_to_1Daudio(twod=self.audio)

    def resampleaudio(self, newfs):
        self.audio = Funcs_used_in_sim.resamplingAudio(audio=self.audio, fs=self.fs, newfs=newfs)

    def make_same_sizes(self, secondsource):
        self.audio, secondsource.audio = Funcs_used_in_sim.make_same_sizes(audio1=self.audio, audio2=secondsource.audio)

    def add_time_delay(self, t_from_start, t_from_end):
        self.audo = Funcs_used_in_sim.add_time_delay(t1=t_from_start, t2=t_from_end, audio=self.audio, fs=self.fs)

    def trim(self, t_start, t_end):
        self.audo = Funcs_used_in_sim.time_trim(audio=self.audio, fs=self.fs, t_start=t_start, t_end=t_end)

    def to_dict(self):
        return {'audio': self.audio,
                 'fs': self.fs,
                 'x': self.x,
                 'y': self.y,
                 'z': self.z,
                 'muted': self.muted}


class microphone():
    def __init__(self, x=0, y=0, z=0, muted=0):
        self.x = x
        self.y = y
        self.z = z
        self.muted = muted

    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0

    def write(self):
        return {'x': self.x, 'y': self.y, 'z': self.z, 'muted': self.muted}

    def to_dict(self):
        return { 'x': self.x,
                 'y': self.y,
                 'z': self.z,
                 'muted': self.muted}


class simulation_space:
    def __init__(self, length=10000, width=10000, height=10000, fs=16000, max_order=1, sources=[], microphones=[],
                 temperature=0, humadity=0, walls=0, floor=0, air_absorption=True, ray_tracing=False):
        self.room_dim = [length, width, height]
        self.fs = fs
        self.walls = walls
        self.floor = floor
        self.max_order = max_order
        self.air_absorption = air_absorption
        self.ray_tracing = ray_tracing

        self.material_values = ['hard_surface', 'brickwork', 'rough_concrete', 'ceramic_tiles', 'concrete_floor',
                                'plasterboard', 'glass_window', 'wood_1.6cm', 'audience_floor', 'stage_floor',
                                'wooden_door', 'carpet_cotton', 'carpet_thin', 'curtains_velvet', 'studio_curtains',
                                'chairs_wooden', 'audience_orchestra_choir', 'facing_brick', 'ceiling_plasterboard',
                                'theatre_audience', 'anechoic']
        self.mat = pra.make_materials(
            ceiling=(self.material_values[walls], 0.1),
            floor=(self.material_values[floor], 0.1),
            east=(self.material_values[walls], 0.15),
            west=(self.material_values[walls], 0.15),
            north=(self.material_values[walls], 0.15),
            south=(self.material_values[walls], 0.15),
        )
        #self.walls = self.material_values[20]
        #self.floor = self.material_values[1]

        self.room = pra.ShoeBox(self.room_dim, fs=self.fs, max_order=self.max_order, materials=self.mat,
                                air_absorption=self.air_absorption, ray_tracing=self.ray_tracing)
        self.list_sources = sources
        self.list_microphones = microphones


    def plot_room(self):
        fig, ax = self.room.plot(mic_marker_size=30)
        ax.set_xlim([0, 10000])
        ax.set_ylim([0, 10000])
        ax.set_zlim([0, 10000])
        plt.show()

    def add_source(self, source):
        self.room.add_source([source.x, source.y, source.z], source.audio)
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
        self.room.add_microphone([mic.x, mic.y, mic.z])
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

    def room_params(self):
        return [self.length, self.width, self.height]


class source_func:
    def __init__(self, duration=0, frequency_parameters={}, x=0, y=0, z=0, muted=0):
        self.duration = duration
        self.frequency_parameters = frequency_parameters
        self.frequency_parameters['freq_ids'] = frequency_parameters['freq_ids']
        self.frequency_parameters['index'] = frequency_parameters['index']
        self.frequency_parameters['parameters'] = frequency_parameters['parameters']
        for i in range(len(self.frequency_parameters['freq_ids'])):
            f_id = self.frequency_parameters['freq_ids'][i]
            self.frequency_parameters['parameters'][f_id] = frequency_parameters['parameters'][f_id]
            self.frequency_parameters['parameters'][f_id]['name'] = frequency_parameters['parameters'][f_id]['name']
            self.frequency_parameters['parameters'][f_id]['frequency'] = frequency_parameters['parameters'][f_id]['frequency']
            self.frequency_parameters['parameters'][f_id]['amplitude'] = frequency_parameters['parameters'][f_id]['amplitude']
            self.frequency_parameters['parameters'][f_id]['phase'] = frequency_parameters['parameters'][f_id]['phase']

        self.x = x
        self.y = y
        self.z = z
        self.muted = muted

    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0

    def to_dict(self):
        return {'duration': duration,
                'frequency_parameters': {'freq_ids': self.frequency_parameters['freq_ids'], 'index': self.frequency_parameters['index'],
                                         'parameters': self.frequency_parameters['parameters']},
                'x': self.x,
                'y': self.y,
                'z': self.z,
                'muted': self.muted}

    def print(self):
        print(self.to_dict())


"""""
class source_func:
    def __init__(self, amplitude=0, fs=0, frequency=0, time=0, phase=0, x=0, y=0, z=0, muted=0):
        self.amplitude = amplitude
        self.fs = fs
        self.frequency = frequency
        self.time = time
        self.phase = phase
        self.x = x
        self.y = y
        self.z = z
        self.muted = muted

    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0

    def to_dict(self):
        return {'amplitude': self.amplitude,
                'fs': self.fs,
                'frequency': self.frequency,
                'time': self.time,
                'phase': self.phase,
                'x': self.x,
                'y': self.y,
                'z': self.z,
                'muted': self.muted}

"""""
class source_wav:
    def __init__(self, filename='', t_start=0, t_end=0, time=0, x=0, y=0, z=0, muted=0):
        self.filename = filename
        self.t_start = t_start
        self.t_end = t_end
        self.time = time
        self.x = x
        self.y = y
        self.z = z
        self.muted = muted

    def set_muted(self):
        self.muted = 1

    def set_unmuted(self):
        self.muted = 0

    def to_dict(self):
        return {'filename': self.filename,
                't_start': self.t_start,
                't_end': self.t_end,
                'time': self.time,
                'x': self.x,
                'y': self.y,
                'z': self.z,
                'muted': self.muted}


def create_source_functional(s: source_func, fs: int):
    F = []
    for i in range(len(s.frequency_parameters['freq_ids'])):
        f_id = s.frequency_parameters['freq_ids'][i]
        dict_f = {}
        dict_f['frequency'] = s.frequency_parameters['parameters'][f_id]['frequency']
        dict_f['amplitude'] = s.frequency_parameters['parameters'][f_id]['amplitude']
        dict_f['phase'] = s.frequency_parameters['parameters'][f_id]['phase']
        F.append(dict_f)

    audio = Funcs_used_in_sim.create_sinewave(fs=fs, duration=s.duration, F_params=F)
    print('audio-', audio)
    return soundsource(audio=audio, fs=fs, x=s.x, y=s.y, z=s.z, muted=s.muted)

"""""
def create_source_functional(s: source_func):
    _, audio = Funcs_used_in_sim.generateSinusoide(amplitude=s.amplitude, fs=s.fs, frequency=s.frequency,
                                                   time=s.time, phase=s.phase)
    return soundsource(audio=audio, fs=s.fs, x=s.x, y=s.y, z=s.z, muted=s.muted)
"""""

def create_source_from_file(s: source_wav, fs: int):
    if s.time != s.t_end-s.t_start:
        s.time = s.t_end-s.t_start

    samp_f, audio = wavfile.read(s.filename)
    audio = Funcs_used_in_sim.time_trim(audio=audio, fs=samp_f, t_start=s.t_start, t_end=s.t_end)
    audio = Funcs_used_in_sim.resamplingAudio(audio=audio, fs=samp_f, newfs=fs)
    source = soundsource(audio=audio, fs=fs, x=s.x, y=s.y, z=s.z, muted=s.muted)
    if source.audio.ndim > 1:
        source.change_to_oneD()
    return source

"""""
class Parser_from_yaml_to_py:
    def __init__(self, config_filename: str):
        self.config_filename = config_filename

    def parse_configs(self):
        with open(self.config_filename) as f:
            return yaml.load(f, Loader=yaml.FullLoader)
"""""


