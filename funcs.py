import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sp
from scipy.io.wavfile import write
import math
import scipy.signal
import pyaudio
import wave
import time


def read_wav(filename="", mmap=True):
    """
    :param filename: string filename
    :param mmap: bool, two-channel or one-channel
    :return: sound_array, fs
    """
    fs, audio = sp.wavfile.read(filename)
    sound_array = []
    if mmap:  # if form is true, the wav file is interleaved stereo file. takes 1st channel
        for i in range(0, len(audio)):
            sound_array.append(audio[i][1])
    else:
        sound_array = audio
    return sound_array, fs

def resamplingAudio(audio, fs, new_fs):
    # taking the nearest integer duration of the signal
    n = math.ceil(len(audio) / fs)
    # Counting the number of added points to the initial signal
    add_to_len = n * fs - len(audio)
    if add_to_len != 0:
        # Adding additional points
        addition = [0] * add_to_len
        audio += addition

    # Number of samples for resampled audio waveform
    new_audio_samples = int(new_fs * len(audio) / fs)

    new_audio = scipy.signal.resample(audio, new_audio_samples)
    return new_audio



play_pause = []
stop = []
def player(filename, new_fs: int, n: int):
    """
    player function modifies your audio's sample frequency, divides an audio into n parts, and for each part
    checks if play, pause and stop buttons are pressed or not.
    :param filename: File name which fs you want to modify
    :param new_fs: Your desired sample frequency
    :param n: Divide an audio into n parts
    :return:
    """
    sound_array, fs = read_wav(filename, mmap=False)
    audio = resamplingAudio(list(sound_array), fs, new_fs)
    write("audio.wav", new_fs, audio.astype(np.int16))

    file_name = wave.open("audio.wav", 'rb')

    length_n = int(len(audio) / n)  # length of each part of a divided audio
    duration = int(len(audio) / new_fs)  # duration of an audio
    time_array = np.arange(0, duration, duration / len(audio))

    # doing fft
    power_spectrum, frequencies_found, t, image_axis = plt.specgram(audio, Fs=new_fs,
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
    while i < len(audio) - length_n:
        if stop == 1:
            i = 0
        while play_pause == 0:
            time.sleep(1)
        file_name.setpos(i)
        frames = file_name.readframes(length_n)
        stream.write(frames)
        minute_second = time_array[i]
        power = powers[i]
        frequency = frequencies_found
        # return minute_second
        i += length_n

    stream.close()
    py_audio.terminate()
    file_name.close()
