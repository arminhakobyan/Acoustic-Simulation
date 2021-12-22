import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import math

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
    if add_to_len != 0 :
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


def generateSinusoide(amplitude, fs, frequency, time = 5, phase = 0):
    # whole time is T
    T = 1/fs
    # count of samples - N
    N = fs*time
    omega = 2*np.pi*frequency
    # time sequency - t_seq
    t_seq = np.arange(N) * T
    y = amplitude * np.sin(omega * t_seq + phase)  # array-like
    return (t_seq, y)
