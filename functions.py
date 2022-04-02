from multiprocessing import Process
import numpy as np
from funcs import read_wav, resamplingAudio
import threading
from threading import Thread
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import pyaudio
import wave
import time

filename = 'C:\\examples_samples_guitar.wav'

sound_array, fs = read_wav(filename, mmap=False)
new_fs = 32000
n = 4
audio = resamplingAudio(list(sound_array), fs, new_fs)
write("audio.wav", new_fs, audio.astype(np.int16))

file_name = wave.open("audio.wav", 'rb')
length_n = int(len(audio) / n)  # length of each part of a divided audio
duration = int(len(audio) / new_fs)  # duration of an audio
time_array = np.arange(0, duration, duration / len(audio))

#  doing fft
power_spectrum, frequencies_found, t, image_axis = plt.specgram(audio, Fs=new_fs,
                                                                mode='magnitude',
                                                                noverlap=0,
                                                                NFFT=1024,
                                                                xextent=(0, np.max(time_array)))
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


if __name__ == "__main__":
    play_pause = 1
    stop = 0
    t = threading.Thread(target=player)
    t.start()
    time.sleep(3)
    play_pause = 0
    time.sleep(2)
    play_pause = 1
    time.sleep(1)
    stop = 1
    time.sleep(3)
    stop = 0

"""
if __name__ == "__main__":
    power = []
    p1 = Process(target=player, args=())
    p2 = Process(target=showing_audiotrack, args=())
    p1.start()
    p2.start()

    p1.join()
    p2.join()
"""

