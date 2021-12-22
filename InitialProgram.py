import pyroomacoustics as pra
import yaml
import sys
import ruamel.yaml
from yaml import FullLoader, SafeDumper
from Sim_room_classes import *


#parser = Parser_from_yaml_to_py('Initial_configs.yaml')
#configs = parser.parse_configs()
with open('test.yaml') as f:
    configs = yaml.load(f, Loader=FullLoader)

room_confs = configs['Room']
sim_room = simulation_room(**room_confs)

s1_confs = configs['Sources']['Source1']['functional_form']
s2_confs = configs['Sources']['Source2']['wav file']
mic_confs = configs['microphones']['mic1']

s1_func = source_func(**s1_confs)
s2_wav = source_wav(**s2_confs)

source1 = create_source_functional(s1_func)
source2 = create_source_from_file(s2_wav)

source1.resampleaudio(newfs=sim_room.fs)
source2.resampleaudio(newfs=sim_room.fs)
source2.make_same_sizes(secondsource=source1)

sim_room.add_source(source1)
sim_room.add_source(source2)

mic1 = microphone(**mic_confs)
sim_room.add_microphone(mic1)

mic2 = microphone(x=20, y=20, z=20, muted=1)
mic2_dic = mic2.to_dict()

#configs['microphones']['mic1'] = mic2_dic

s3 = source_func(amplitude=100, fs=100, frequency=100, time=5, phase=0, x=100, y=100, z=100, muted=0)
s3_func_dict = s3.to_dict()

sim_params = configs['Simulation parameters']

with open('test.yaml') as f:
    data = yaml.load(f, Loader=FullLoader)
with open('test.yaml', 'w') as f:
    data['microphones']['mic2'] = mic2_dic
    data['Sources']['Source3'] = {}
    data['Sources']['Source3']['functional_form'] = s3_func_dict
    #data['Sources']['Source4'] = s1
    yaml.dump(data, f, sort_keys=False, indent=4)











"""""
sim_room = simulation_room(length=10000, width=10000, height=10000, sampf=16000, max_order=1, sources=[], microphones=[],
                 air_absorption=True, ray_tracing=False)

source1 = create_source_functional(amplitude=5000, fs=11000, frequency=5000, time=5, phase=0, x=5000, y=10,
                                                                                            z=10, muted=0)
source2 = create_source_from_file(filename='C:\passing-car-and-urban-ambience.wav', samp_f=16000, t=5, t0=0, t1=5, x=5000,
                                                                                 y=9990, z=10, muted=0)

source1.resampleaudio(newfs=sim_room.fs)
source2.resampleaudio(newfs=sim_room.fs)

source2.make_same_sizes(secondsource=source1)

sim_room.add_source(source1)
sim_room.add_source(source2)

mic = microphone(pos_x=4090, pos_y=10, pos_z=10, muted=0)
sim_room.add_microphone(mic)
"""""





