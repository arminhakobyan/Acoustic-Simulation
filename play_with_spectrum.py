import numpy as np
from funcs import read_wav
import matplotlib.pyplot as plt
import pyaudio
import wave
import time

filename = 'C:\\examples_samples_guitar.wav'

sound_array, fs = read_wav(filename, mmap=False)
# new_fs = 32000
# audio = resamplingAudio(list(sound_array), fs, new_fs)
# print(len(audio))
# write("audio.wav", new_fs, audio.astype(np.int16))
# n = int(len(audio) / 1024)
# file_name = wave.open("audio.wav", 'rb')
length_n = 1024  # length of each part of a divided audio
duration = int(len(sound_array / fs))  # duration of an audio
time_array = np.arange(0, duration, duration / len(sound_array))

# doing fft
degree = 11
fft_points = (2 ** degree)
power_spectrum, frequencies_found, _, _ = plt.specgram(sound_array, Fs=fs,
                                                       mode='magnitude',
                                                       noverlap=0,
                                                       NFFT=fft_points,
                                                       xextent=(0, np.max(time_array)))
powers = np.transpose(power_spectrum)

# max_value_of_each_spec = []
# for i in range(len(powers)):
# max_value_of_each_spec.append(max(powers[i]))
# max_of_all_spec = max(max_value_of_each_spec)

play_pause = 1
stop = 0
power = []

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
x = frequencies_found
y = powers[0]
ax.set_ylim([0, 10000])
line1, = ax.plot(x, y, 'c-')


def player():
    global sound_array, length_n, duration, time_array, fft_points
    file_name = wave.open('C:\\examples_samples_guitar.wav', 'rb')
    # length of each part of a divided audio
    global play_pause
    global stop
    py_audio = pyaudio.PyAudio()
    stream = py_audio.open(format=py_audio.get_format_from_width(file_name.getsampwidth()),
                           channels=file_name.getnchannels(),
                           rate=file_name.getframerate(),
                           output=True)
    i = 0
    while i < len(sound_array) - length_n:
        if stop == 1:
            i = 0
        while play_pause == 0:
            time.sleep(1)
        global power
        power = []
        for j in range(int(i / fft_points), int((i + length_n) / fft_points)):
            power.append(powers[j])
        file_name.setpos(i)

        frames = file_name.readframes(length_n)
        stream.write(frames)
        for k in range(len(power)):
            line1.set_ydata(power[k])
            fig.canvas.draw()
            fig.canvas.flush_events()
            k += length_n

        i += length_n
    stream.close()
    py_audio.terminate()
    file_name.close()


player()

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