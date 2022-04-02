import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import math
from scipy.io.wavfile import write
from Sim_room_classes import *

"""""
This file is created by Armine for wellbeing of our cute coorporation: 
"""""

# convert the 2 dimensional audio to the 1 dimensional
def twoDaudio_to_1Daudio(twod):
    # taking an one dimensional array with 0 values
    oned = [0]*(len(twod))
    # give the first values of 2d array to 1d array
    for i in range(len(twod)):
        oned[i] = twod[i][1]

    return oned


def resamplingAudio(audio, fs, newfs):
    # taking the nearest integre duration of the signal
    n = math.ceil(len(audio) / fs)
    # Counting the number of added points to the initial signal
    add_to_len = n * fs - len(audio)
    if add_to_len != 0:
        # Adding additional points
        audio += [0]*add_to_len

    # Number of samples for resampled audio waveform
    new_audio_samples = int(newfs * len(audio) / fs)

    new_audio = scipy.signal.resample(audio, new_audio_samples)
    return new_audio


# make both of audios to the same - the shortest size of audio1 and audio2
def make_same_sizes(audio1, audio2):
    if len(audio1) > len(audio2):
        audio = [0]*len(audio1)
        for i in range(len(audio2)):
            audio[i] = audio2[i]
        return (audio1, audio)
    else:
        audio = [0] * len(audio2)
        for i in range(len(audio1)):
            audio[i] = audio1[i]
        return(audio, audio2)


# adding t1 time from the start and t2 to the end of the audio signal
def add_time_delay(t1, t2, audio, fs):
    #count of samples needed to add from the start to the audio
    n1 = int(fs * t1)
    # count of samples needed to add to the end of the audio
    n2 = int(fs * t2)

    # the new audio will be of (n1 + len(audio) + n2)-length,,
    # creating the array with 0 values, and then filling it with needed values
    new_audio = [0] * (n1 + len(audio) + n2)
    for i in range(len(audio)):
        new_audio[i + n1] = audio[i]

    return new_audio

# cutting the audio taking (tsart-tend) part
def time_trim(audio, fs, t_start, t_end):
    whole_time = len(audio) / fs
    t2 = whole_time - t_end
    n1 = int(fs * t_start)
    n2 = int(fs * t2)

    new_audio = [0] * (len(audio) - n1 - n2)
    for i in range(len(new_audio)):
        new_audio[i] = audio[i + n1]

    return new_audio


def generateSinusoide(amplitude=0, fs=0, frequency=0, time = 5, phase = 0):
    # whole time is t
    t = 1/fs
    # count of samples - n
    n = fs*time
    omega = 2*np.pi*frequency
    # time sequency - t_seq
    t_seq = np.arange(n) * t
    y = amplitude * np.sin(omega * t_seq + phase)  # array-like
    return (t_seq, y)


# F - list of dictionaries of keys - Amplitude, Frequency, Phase
def create_sinewave(fs=0, duration=0, F_params=[]):
    time = np.arange(0, duration, 1 / fs)

    sinewave = np.empty(len(time))
    for i in range(len(F_params)):
        sinewave += F_params[i]['amplitude'] * np.sin(2 * np.pi * F_params[i]['frequency'] * time + F_params[i]['phase'])

    print('sinwave-', sinewave)
    return sinewave


"""""
play_pause: int
stop: int

def player(s: soundsource):
    samples = 1024  #count samples of each chunk

    # length_n - samples
    write("audio.wav", s.fs, s.audio.astype(np.int16))
    file_name = wave.open("audio.wav", 'rb')

    duration = int(len(s.audio) / s.fs)  # duration of an audio
    time_array = np.arange(0, duration, duration / len(s.audio))

    fft_points = int(len(s.audio) / 1024)
    # doing fft
    power_spectrum, frequencies_found, t, image_axis = plt.specgram(s.audio, Fs=s.fs,
                                                                    mode='magnitude',
                                                                    noverlap=0,
                                                                    NFFT=fft_points,
                                                                    xextent=(0, np.max(time_array)))
    powers = np.transpose(power_spectrum)

    global play_pause
    global stop
    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(format=py_audio.get_format_from_width(file_name.getsampwidth()),
                           channels=file_name.getnchannels(),
                           rate=file_name.getframerate(),
                           output=True)
    i = 0
    while i < len(s.audio) - samples:
        if stop == 1:
            i = 0
        while play_pause == 0:
            time.sleep(1)
        file_name.setpos(i)
        frames = file_name.readframes(samples)
        stream.write(frames)
        minute_second = time_array[i]
        power = powers[i]
        frequency = frequencies_found
        # return minute_second
        i += samples

    stream.close()
    py_audio.terminate()
    file_name.close()
#---------------------------------------------------------------

play_pause = 1
stop = 0
power = []
powers = np.transpose(power_spectrum)
powers = list(powers)
frequencies_found = list(frequencies_found)

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
x = frequencies_found
y = powers[0]
ax.set_ylim([0, 10000])
line1, = ax.plot(x, y, 'c-')


def player(filename=filename, n=34, new_fs=32000):
    sound_array, fs = read_wav(filename, mmap=False)
    audio = resamplingAudio(list(sound_array), fs, new_fs)
    write("audio.wav", new_fs, audio.astype(np.int16))

    file_name = wave.open("audio.wav", 'rb')
    length_n = int(len(audio) / n)  # length of each part of a divided audio
    duration = int(len(audio) / new_fs)  # duration of an audio
    time_array = np.arange(0, duration, duration / len(audio))

    #  doing fft
    global frequencies_found
    global power_spectrum
    global powers

    power_spectrum, frequencies_found, _, _ = plt.specgram(audio, Fs=new_fs,
                                                           mode='magnitude',
                                                           noverlap=0,
                                                           NFFT=1024,
                                                           xextent=(0, np.max(time_array)))
    powers = np.transpose(power_spectrum)

    global play_pause
    global stop
    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(format=py_audio.get_format_from_width(file_name.getsampwidth()),
                           channels=file_name.getnchannels(),
                           rate=file_name.getframerate(),
                           output=True)

    i = 0
    max_value_of_each_spec = []
    for i in range(len(powers)):
        max_value_of_each_spec.append(max(powers[i]))
        max_of_all_spec = max(max_value_of_each_spec)
    while i < len(audio) - length_n:
        if stop == 1:
            i = 0
        while play_pause == 0:
            time.sleep(1)
        if play_pause == 1:
            stop = 0
        global power
        power = []
        for j in range(int(i / 1024), int((i + length_n) / 1024)):
            power.append(powers[j])
        file_name.setpos(i)
        # FFT of the frame, write to global variable
        frames = file_name.readframes(length_n)
        stream.write(frames)
        audio = list(audio)
        for k in range(10):
            line1.set_ydata(power[k])
            fig.canvas.draw()
            fig.canvas.flush_events()
            k += length_n
        # minute_second = time_array[i]
        # power = powers[i]
        # frequency = frequencies_found
        # return minute_second

        i += length_n

    stream.close()
    py_audio.terminate()
    file_name.close()
    
"""""
