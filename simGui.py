from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import filedialog
# from two_diff_sinusoide_sound import *
from sim_room_classes import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from scipy.io import wavfile
import pyroomacoustics as pra
import matplotlib.pyplot as plt
import pygame
from functions_for_sim import *
from buffer import *
from simulation_data import *
from package import *
import sys


# for sources window - data - data[Sources],  entry_list - entries(amplitude, freq.. to input),
#  event - combobox event to change source
#  for microphones - data - data[Microphones], entry_list - entries(pos_x, pos_y.. to input)


def create_new_simulation_room():
    global Data

    room_sim = simulation_room(length=Data['Room'][0], width=Data['Room'][1], height=Data['Room'][2],
                               sampf=Data['Simulation parameters'][0], max_order=Data['Simulation parameters'][1],
                               air_absorption=bool(Data['Simulation parameters'][5]),
                               ray_tracing=bool(Data['Simulation parameters'][6]),
                               sources=[], microphones=[])

    for i in range(Data['Count Sources']):
        if Data['Sources'][i][5] == 0:
            source = soundsource(audio=Data['Sources'][i][0], samp_f=Data['Sources'][i][1], pos_x=Data['Sources'][i][2],
                                 pos_y=Data['Sources'][i][3], pos_z=Data['Sources'][i][4], muted=Data['Sources'][i][5])

            room_sim.add_source(source)

    Data['Active Sources'] = room_sim.list_sources

    for i in range(Data['Count Microphones']):
        if Data['Microphones'][i][3] == 0:
            room_sim.add_microphone(microphone(pos_x=Data['Microphones'][i][0], pos_y=Data['Microphones'][i][1],
                                               pos_z=Data['Microphones'][i][2], muted=Data['Microphones'][i][3]))

    # Data['Array Microphones'] = room_sim.list_microphones
    Data['Active Microphones'] = room_sim.list_microphones

    return room_sim


def plot_room():
    room = create_new_simulation_room()

    fig_room, ax = room.room.plot(mic_marker_size=30, figsize=(6, 3.5))
    ax.set_xlim([0, room.room_dim[0] + 5])
    ax.set_ylim([0, room.room_dim[1] + 5])
    ax.set_zlim([0, room.room_dim[2] + 5])

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig_room, master=root_window)
    canvas.draw()
    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(x=1030, y=-10)     #1330
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, root_window)
    # placing the toolbar on the Tkinter window
    toolbar.place(x=1060, y=340)            #1390


def plot_sin_sound():
    sim_room = create_new_simulation_room()

    fig = Figure(figsize=(6, 2.3), dpi=100)
    sin_audios = []
    if sim_room.list_sources == []:
        exit()

    count_sources = len(sim_room.active_sources())
    for i in range(count_sources):
        # _, audio = generateSinusoide(amplitude=Data['Sources'][i][0], fs=Data['Sources'][i][1],
        #                        frequency=Data['Sources'][i][2], phase=Data['Sources'][i][3])
        # sin_audios.append(audio)
        sin_audios.append(Data['Sources'][i][0])

    room_fs = Data['Simulation parameters'][0]

    x_s = []
    for j in range(count_sources):
        x = np.linspace(0, len(sin_audios[j]) / room_fs, num=len(sin_audios[j]))
        x_s.append(x)

    plot1 = fig.add_subplot(111)
    for i in range(count_sources):
        plot1.plot(x_s[i], sin_audios[i])

    canvas = FigureCanvasTkAgg(fig, master=root_window)
    canvas.draw()
    canvas.get_tk_widget().place(x=1030, y=390)      #x=1330
    toolbar = NavigationToolbar2Tk(canvas, root_window)
    toolbar.place(x=1060, y=625)         #x=1390


def plot_sin_mic():
    sim_room = create_new_simulation_room()

    fig = Figure(figsize=(6, 2.3), dpi=100)
    mic = scipy.io.wavfile.read(project_path + "mic1.wav")
    mic_audio = mic[1]

    #room_fs = Data['Simulation parameters'][0]
    t = np.linspace(0, len(mic_audio) / sim_room.fs, num=len(mic_audio))
    plot1 = fig.add_subplot(111)
    plot1.plot(mic_audio)

    canvas = FigureCanvasTkAgg(fig, master=root_window)
    canvas.draw()
    canvas.get_tk_widget().place(x=1030, y=665)
    toolbar = NavigationToolbar2Tk(canvas, root_window)
    toolbar.place(x=1060, y=892)


# initial general window for simulation project
root_window = tkinter.Tk()
root_window.geometry('1900x950')
root_window.title("Simulation App")
menubar = tkinter.Menu(root_window)

plot_sin_sound()

plot_room()


#  Room top level window
def open_room_window():
    room_win = Toplevel(root_window)
    room_win.geometry('480x510')
    room_win.title('Room')

    global Data

    def fill_entries():
        for i in range(len(arr_entries)):
            arr_entries[i].insert(END, Data['Room'][i])

    separator1 = ttk.Separator(room_win, orient='horizontal')
    separator1.place(relx=0, rely=0.3, relwidth=1, relheight=1)
    separator2 = ttk.Separator(room_win, orient='horizontal')
    separator2.place(relx=0, rely=0.6, relwidth=1, relheight=1)
    sizes_label = Label(room_win, text='Sizes', font=15).place(x=15, y=10)
    env_label = Label(room_win, text='Environment', font=15).place(x=15, y=170)
    surface_mat = Label(room_win, text="Surface materials", font=15).place(x=15, y=330)
    lb1 = tkinter.Label(room_win, text='Length', font=6).place(x=115, y=40)
    l1 = tkinter.Label(room_win, text='m').place(x=315, y=40)
    length_entry = tkinter.Entry(room_win)
    length_entry.place(x=180, y=40)
    lb2 = tkinter.Label(room_win, text='Width', font=6).place(x=115, y=70)
    l2 = tkinter.Label(room_win, text='m').place(x=315, y=70)
    width_entry = tkinter.Entry(room_win)
    width_entry.place(x=180, y=70)
    lb3 = tkinter.Label(room_win, text='Height', font=6).place(x=115, y=100)
    l3 = tkinter.Label(room_win, text='m').place(x=315, y=100)
    height_entry = tkinter.Entry(room_win)
    height_entry.place(x=180, y=100)
    surface_wall_mat_label = Label(room_win, text='Walls', font=6).place(x=115, y=370)
    surface_floor_mat_label = Label(room_win, text='Floor', font=6).place(x=115, y=400)
    temp_label = Label(room_win, text='Temperature', font=6).place(x=55, y=200)
    temp_entry = tkinter.Entry(room_win)
    temp_entry.place(x=175, y=200)
    temp_unit_label = Label(room_win, text='Celsius').place(x=310, y=200)
    humadity_label = Label(room_win, text='Humadity', font=6).place(x=55, y=230)
    humd_unit_label = Label(room_win, text='%').place(x=310, y=230)
    humd_entry = tkinter.Entry(room_win)
    humd_entry.place(x=175, y=230)

    arr_entries = [length_entry, width_entry, height_entry, temp_entry, humd_entry]

    fill_entries()

    def change_walls(event):
        wall = event.widget.get()
        Data['Room'][5] = Data['Material values'].index(wall)

    def change_floor(event):
        floor = event.widget.get()
        Data['Room'][6] = Data['Material values'].index(floor)

    def get_room_values():
        for i in range(len(arr_entries)):
            Data['Room'][i] = int(arr_entries[i].get())
        Data['Room'][5] = Data['Material values'].index(mat_walls.get())
        Data['Room'][6] = Data['Material values'].index(mat_floor.get())
        plot_room()
        room_win.destroy()

    mat_walls = tkinter.StringVar()
    mat_choosen_walls = ttk.Combobox(room_win, width=25, textvariable=mat_walls)
    mat_choosen_walls['values'] = Data['Material values']
    mat_choosen_walls.place(x=180, y=370)
    mat_floor = tkinter.StringVar()
    mat_choosen_floor = ttk.Combobox(room_win, width=25, textvariable=mat_floor)
    mat_choosen_floor['values'] = Data['Material values']
    mat_choosen_floor.place(x=180, y=400)
    mat_choosen_walls.current(Data['Room'][5])
    mat_choosen_floor.current(Data['Room'][6])

    mat_choosen_walls.bind('<<ComboboxSelected>>', change_walls)
    mat_choosen_floor.bind('<<ComboboxSelected>>', change_floor)

    bt_accept = tkinter.Button(room_win, text='Accept', font=5, width=6,
                               height=1, command=get_room_values).place(x=365, y=460)
    bt_cancel = tkinter.Button(room_win, text='Cancel', font=5, width=6,
                               height=1, command=room_win.destroy).place(x=285, y=460)

    room_win.mainloop()


# Source top level window ------------------------------------------------------------
source_opt = tkinter.StringVar()


def open_source_window():
    source_win = Toplevel(root_window)
    source_win.geometry('920x280')
    source_win.title('Source')

    bt_label = tkinter.Label(source_win, text='Sources', font=12, height=1)
    bt_label.place(x=20, y=10)
    amplitude_label = tkinter.Label(source_win, text='Amplitude', width=15, height=1, font=5)
    amplitude_label.place(x=270, y=8)  # x-230
    amplitude_entry = tkinter.Entry(source_win, width=15)
    amplitude_entry.place(x=415, y=13)
    sampFreq_label = tkinter.Label(source_win, text='Sampling frequency(fs)', width=25, height=1, font=5)
    sampFreq_label.place(x=510, y=8)
    sampFreq_entry = tkinter.Entry(source_win, width=15)
    sampFreq_entry.place(x=760, y=13)
    freq_label = tkinter.Label(source_win, text='Frequency', width=15, height=1, font=5)
    freq_label.place(x=270, y=40)
    freq_entry = tkinter.Entry(source_win, width=15)
    freq_entry.place(x=415, y=43)
    phase_label = tkinter.Label(source_win, text='Phase', width=15, height=1, font=5)
    phase_label.place(x=600, y=40)
    phase_entry = tkinter.Entry(source_win, width=15)
    phase_entry.place(x=760, y=43)
    time_label = tkinter.Label(source_win, text='Time', width=15, height=1, font=5)
    time_label.place(x=600, y=72)
    time_entry = tkinter.Entry(source_win, width=15)
    time_entry.place(x=760, y=75)
    pos_label = tkinter.Label(source_win, text='Position', width=15, height=1, bd=5, font=5).place(x=230, y=145)
    posx_label = tkinter.Label(source_win, text='X', width=5, font=2).place(x=375, y=145)
    posy_label = tkinter.Label(source_win, text='Y', width=5, font=2).place(x=520, y=145)
    posz_label = tkinter.Label(source_win, text='Z', width=5, font=2).place(x=665, y=145)
    posx_entry = tkinter.Entry(source_win, width=15)
    posx_entry.place(x=415, y=151)
    posy_entry = tkinter.Entry(source_win, width=15)
    posy_entry.place(x=560, y=151)
    posz_entry = tkinter.Entry(source_win, width=15)
    posz_entry.place(x=705, y=151)

    t_start_label = tkinter.Label(source_win, text="T start", width=7, height=1, font=1)
    t_start_entry = tkinter.Entry(source_win, width=10)
    t_end_label = tkinter.Label(source_win, text="T end", width=7, height=1, font=1)
    t_end_entry = tkinter.Entry(source_win, width=10)
    check_mute = tkinter.IntVar()

    # label_file_explorer = tkinter.LabelFrame(source_win, text="Wav file", width=80, height=3, font=1)
    wavf_entry = tkinter.Entry(source_win, width=45)
    file_opened = ""
    wavf_entry.insert(0, file_opened)

    # all entries in this window
    # entries = [[None for entry in range(9)] for form in range(2)]     # is a 2d array(functional entries and wav file - form=0/1)
    # entries = [[None]*9]*2
    entries = []
    entries_func = [None] * 9
    entries_file = [None] * 9
    entries_func = (amplitude_entry, sampFreq_entry, freq_entry, phase_entry, time_entry, posx_entry, posy_entry,
                    posz_entry, check_mute)
    entries_file = (wavf_entry, sampFreq_entry, t_start_entry, t_end_entry, time_entry, posx_entry, posy_entry,
                    posz_entry, check_mute)
    entries.append(entries_func)
    entries.append(entries_file)

    buffer_sources = BufferSources(prev_obj_index=0, source_forms=source_forms, data=data_buffer, entries=entries)
    # if all sources are removed, there is no previous object, so prev_obj_index = None
    if len(buffer_sources.data) == 0:
        buffer_sources.prev_obj_index = None
    else:
        # filling entries with data_buffer initial values for first source
        buffer_sources.fill_entries(0, source_forms[0])

 #when source changes, previous source's parameters must be saved in the buffer, then fill new source's parameters
 # in the entries
    def source_option_change(event):
        if event.widget.get() == 'Add Source':
            ind = sources.index('Add Source')
            sources.insert(ind, 'Source ' + str(ind + 1))    #adding new source in sources widget
            source_cb['values'] = sources
            event.widget.set(sources[ind])
            buffer_removed.append(0)               # adding a new element in buffer (for removed objects)- indicating not removed
            buffer_sources.source_forms.append(0)  # adding a new source form(by default 0) in the source_forms array
            buffer_newsource = []
            buffer_func_newsource = [0]*9       #functional form parameters for new source
            buffer_file_newsource = [None]*9    #file form parameters for new source
            buffer_file_newsource[0] = ""
            for i in range(8):
                buffer_file_newsource[i+1] = 0
            buffer_newsource.append(buffer_func_newsource)
            buffer_newsource.append(buffer_file_newsource)
            buffer_sources.data.append(buffer_newsource)
            remove_btn['text'] = 'Remove'
            for i in range(len(buffer_sources.data[0])):  # by default new source is a functional, so form=0
                buffer_sources.data[0][i].append(0)       # adding a new column in data_buffer for a new object
        next_oject_index = sources.index(event.widget.get())
        if buffer_sources.prev_obj_index != None:
            if remove_btn['text'] == 'Removed':
                buffer_removed[buffer_sources.prev_obj_index] = 1
            if buffer_sources.source_forms[next_oject_index] == 0:
                select_functional_form()
            else:
                select_wavfile_form()
        if buffer_removed[next_oject_index] == 1:
            remove_btn['text'] = 'Removed'
        else:
            remove_btn['text'] = 'Remove'
        buffer_sources.prev_obj_index = next_oject_index

    # in the end, when you click accept, all the buffer data must save in the general data, and then close window
    def get_values():
        Data['Count Active Sources'] = 0
        count_removed = 0
        for i in range(len(buffer_removed)):
            if buffer_removed[i] == 1:
                remove_source(i - count_removed)
                count_removed += 1
        # remove from buffer_Removed all 1-s
        Data['Count Sources'] = len(sources) - 1
        try:
            while True:
                buffer_removed.remove(1)
        except ValueError:
            pass
        if len(sources) > 1:
            if remove_btn['text'] == 'Remove':
                buffer_sources.read_from_entries()
            for i in range(len(sources) - 1):
                if buffer_sources.data[i][0][8] == 0:        #or buffer_sources.data[i][1][8] if muted in 0 form, then muted in 1 form too
                    Data['Count Active Sources'] += 1
                else:
                    #m = buffer_sources.data[i][0][8] ^ buffer_sources.data[i][1][8]   # xor
                    Data['Sources'][i][5] = 1
            buffer_sources.transfer_to_general_data(Data['Sources'])
        plot_room()
        if Data['Count Active Sources'] != 0:
            plot_sin_sound()
        #source_win.destroy()

    def get_values_and_destroy():
        get_values()
        source_win.destroy()

    def remove_source(s_index):
        if s_index > 0:
            buffer_sources.prev_obj_index -= 1
        elif len(buffer_sources.data) == 1:
            buffer_sources.prev_obj_index = None
        else:
            buffer_sources.prev_obj_index = 0
        buffer_sources.data.pop(s_index)       #buffer_sources.data.remove(buffer_sources.data[s_index])
        sources.pop(s_index)
        source_cb['values'] = sources
        buffer_sources.source_forms.pop(s_index)


    sources = []
    count_sources = Data['Count Sources']
    for i in range(count_sources):
        sources.append('Source ' + str(i + 1))
    sources.append('Add Source')  # sources = ('Source 1', 'Source 2', 'Add Source')

    # array of bools indicated for each source is removed or not / 0-not, 1-yes
    buffer_removed = [0] * (len(sources) - 1)

    global source_opt
    # source_opt = tkinter.StringVar()
    source_opt.set("Select from list")
    source_cb = ttk.Combobox(source_win, width=18, height=60, textvariable=source_opt)
    source_cb['values'] = sources
    source_cb.current(0)
    source_cb['state'] = 'readonly'
    source_cb.place(x=110, y=12)
    source_cb.bind('<<ComboboxSelected>>', source_option_change)

    if len(sources) == 0:
        source_cb.current('Add Source')

    def select_muted():
        if check_mute.get() == 1:
            check_mute_btn.select()
        else:
            check_mute_btn.deselect()

    def change_remove_btn_text():
        remove_btn['text'] = 'Removed'
        buffer_removed[sources.index(source_opt.get())] = 1
        print(buffer_removed)

    def browse_wavfile(event=None):
        file_opened = filedialog.askopenfilename(initialdir="/", title="Select a file",
                                                 filetypes=(("Wav files", "*.wav*"), ("all files", "*.*")))  # filename
        wavf_entry.insert(0, file_opened)


    explorer_btn = tkinter.Label(source_win, text="Browse wav file", font=1)
    explorer_btn.bind('<Button-1>', browse_wavfile)

    def forget_functional_entries_place_file():
        amplitude_label.place_forget()
        freq_label.place_forget()
        sampFreq_label.place_forget()
        phase_label.place_forget()
        amplitude_label.place_forget()
        for i in range(4):
            entries_func[i].place_forget()

        wavf_entry.place(x=455, y=30)
        explorer_btn.place(x=280, y=20)
        t_start_label.place(x=290, y=80)
        t_start_entry.place(x=370, y=85)
        t_end_label.place(x=450, y=80)
        t_end_entry.place(x=530, y=85)

    def forget_wavfile_entries_place_functional():
        wavf_entry.place_forget()
        explorer_btn.place_forget()
        t_start_label.place_forget()
        t_end_label.place_forget()

        for i in range(3):
            entries_file[i+1].place_forget()

        amplitude_label.place(x=270, y=8)
        amplitude_entry.place(x=415, y=13)
        freq_label.place(x=270, y=40)
        freq_entry.place(x=415, y=43)
        sampFreq_label.place(x=510, y=8)
        sampFreq_entry.place(x=760, y=13)
        phase_label.place(x=600, y=40)
        phase_entry.place(x=760, y=43)

        # select wav file form, will be deleted functional entries and place entries corresponding to wav file form
        # values in functional entries will be saved in buffer

    # when choose wav file form of source, functional entries will be forgotten, and will be placed entries for
    # wav file form parameters,,  then functional parameters will be saved in buffer_source in corresponding form
    # wav file parameters will be filled in entries
    def select_wavfile_form():
        buffer_sources.read_from_entries()
        forget_functional_entries_place_file()
        source_ind = sources.index(source_cb.get())
        buffer_sources.source_forms[source_ind] = 1
        v.set(1)         #for radiobutton functional/wav file to set wav file form
        # source form changes from functional to wav file form
        # fill wav file entries with values saved in buffer, or default values
        buffer_sources.fill_entries(source_ind, 1)
        select_muted()

        """""
        for i in range(len(buffer_sources.entries[1])):
            #print(i)
            if i == 0:                                             # filename
                #label_opened_file.configure(text="File opened: " + buffer_sources.entries[1][0], font=1)
                wavf_entry.insert(0, buffer_sources.entries[1][0])
            elif i == 8:
                buffer_sources.entries[1][i].set(buffer_sources.data[source_ind][1][i])
            else:
                print(i)
                buffer_sources.entries[1][i].insert(END,
                                                    buffer_sources.data[source_ind][1][i])
        """""

    def select_functional_form():
        buffer_sources.read_from_entries()
        forget_wavfile_entries_place_functional()
        source_ind = sources.index(source_cb.get())
        buffer_sources.source_forms[source_ind] = 0
        v.set(0)        #for radiobutton functional/wav file to set functional form
        # soruce form changes from wav file form to functional
        # fill functional entries with values saved in buffer, or default values
        buffer_sources.fill_entries(source_ind, 0)
        select_muted()


    if len(buffer_sources.data) == 0:
        v = StringVar(source_win, '0')
    else:
        v = StringVar(source_win, str(source_forms[0]))
    forms = {"Functional": "0", "Wav file": "1"}


    # buttons for choosing file form or functional
    func_radiobtn = Radiobutton(source_win, text="Functional", variable=v, value=0, font=1,
                                command=select_functional_form)
    func_radiobtn.place(x=25, y=60)
    file_radiobtn = Radiobutton(source_win, text="Wav file", variable=v, value=1, font=1, command=select_wavfile_form)
    file_radiobtn.place(x=25, y=95)

    mute_label = Label(source_win, text='Muted', font=6).place(x=25, y=145)
    current_s_ind = buffer_sources.prev_obj_index
    if len(buffer_sources.data) == 0:
        check_mute = 0       # Muted=0 - means active / 1-means disactive
    else:
        check_mute.set(buffer_sources.data[current_s_ind][source_forms[current_s_ind]][8])
    check_mute_btn = Checkbutton(source_win, variable=check_mute, onvalue=1, offvalue=0, command=select_muted)
    check_mute_btn.place(x=80, y=147)


    if len(buffer_sources.data) != 0:
        if source_forms[0] == 0:
            select_functional_form()
        else:
            select_wavfile_form()
    else:
        forget_wavfile_entries_place_functional()

    remove_btn = tkinter.Button(source_win, text='Remove', font=5, width=8, height=1,
                                command=change_remove_btn_text)
    remove_btn.place(x=25, y=195)

    bt_apply = tkinter.Button(source_win, text='Apply', font=5, width=10,
                               height=1, command=get_values).place(x=365, y=195)
    bt_ok = tkinter.Button(source_win, text='OK', font=5, width=5,
                              height=1, command=get_values_and_destroy).place(x=550, y=195)
    bt_cancel = tkinter.Button(source_win, text='Cancel', font=5, width=6,
                               height=1, command=source_win.destroy).place(x=475, y=195)

    source_win.mainloop()


# Microphone top level window ------------------------------------------------------------
def open_microphone_window():
    mic_win = Toplevel(root_window)
    mic_win.geometry('770x200')
    mic_win.title('Microphone')

    mic_label = tkinter.Label(mic_win, text='Microphones', font=12, height=1).place(x=15, y=10)
    pos_label = tkinter.Label(mic_win, text='Position', font=10).place(x=15, y=110)
    posx_label = tkinter.Label(mic_win, text='X', width=5, font=2).place(x=75, y=110)
    posy_label = tkinter.Label(mic_win, text='Y', width=5, font=2).place(x=210, y=110)
    posz_label = tkinter.Label(mic_win, text='Z', width=5, font=2).place(x=345, y=110)
    posx_entry = tkinter.Entry(mic_win, width=15)
    posx_entry.place(x=115, y=115)
    posy_entry = tkinter.Entry(mic_win, width=15)
    posy_entry.place(x=250, y=115)
    posz_entry = tkinter.Entry(mic_win, width=15)
    posz_entry.place(x=385, y=115)
    check_mute = tkinter.IntVar()

    wavf_entry = tkinter.Entry(mic_win, width=45)

    arr_of_entries = [posx_entry, posy_entry, posz_entry, check_mute]

    buffer_mics = BufferMicrophones(prev_obj_index=0, data=Data['Microphones'], entries=arr_of_entries)
    if len(buffer_mics.data) == 0:
        buffer_mics.prev_obj_index = None
    else:
        buffer_mics.fill_entries()

    def mic_option_change(event):
        if event.widget.get() == 'Add Microphone':
            ind = mics.index('Add Microphone')
            mics.insert(ind, 'Microphone ' + str(ind + 1))
            buffer_removed.append(0)
            mic_cb['values'] = mics
            event.widget.set(mics[ind])
            remove_btn['text'] = 'Remove'
            new_mic = [0]*4
            buffer_mics.data.append(new_mic)
        next_oject_index = mics.index(event.widget.get())
        if buffer_mics.prev_obj_index != None:
            if remove_btn['text'] == 'Remove':
                buffer_mics.read_from_entries()
            else:
                buffer_removed[buffer_mics.prev_obj_index] = 1
        if buffer_removed[next_oject_index] == 1:
            remove_btn['text'] == 'Removed'
        else:
            remove_btn['text'] == 'Remove'
        buffer_mics.prev_obj_index = next_oject_index
        buffer_mics.fill_entries()


    def get_values():
        Data['Count Active Microphones'] = 0
        count_removed = 0
        for i in range(len(buffer_removed)):
            if buffer_removed[i] == 1:
                remove_mic(i - count_removed)
                count_removed += 1
        Data['Count Microphones'] = len(mics) - 1
        try:
            while True:
                buffer_removed.remove(1)
        except ValueError:
            pass
        if len(mics) > 1:
            if remove_btn['text'] == 'Remove':
                buffer_mics.read_from_entries()
            for i in range(len(mics) - 1):
                if buffer_mics.data[i][3] == 0:
                    Data['Count Active Microphones'] += 1
                else:
                    Data['Microphones'][i][3] = 1
            buffer_mics.transfer_to_general_data(Data['Microphones'])
        plot_room()
        if Data['Count Active Microphones'] != 0:
            plot_sin_mic()


    def get_values_and_destroy():
        get_values()
        mic_win.destroy()

    def remove_mic(m_index):
        if m_index > 0:
            buffer_mics.prev_obj_index -= 1
        elif len(buffer_mics.data) == 1:
            buffer_mics.prev_obj_index = None
        else:
            buffer_mics.prev_obj_index = 0
        buffer_mics.data.pop(m_index)
        mics.pop(m_index)
        mic_cb['values'] = mics


    pygame.mixer.init()

    def play_mic():
        wavf_entry.place()
        file_opened = ""
        wavf_entry.insert(0, file_opened)
        pygame.mixer.music.load(project_path + "mic1.wav")
        pygame.mixer.music.play()

    def stop_play_mic():
        pygame.mixer.music.load(project_path + "mic1.wav")
        pygame.mixer.music.stop()

    def pause_unpause_mic():
        if bt_pause['text'] == "Pause":
            bt_pause['text'] = "Unpause"
            pygame.mixer.music.pause()
        else:
            bt_pause['text'] = "Pause"
            pygame.mixer.music.unpause()
        #pygame.mixer.music.load(project_path + "mic1.wav")



    mics = []
    count_mics = Data['Count Microphones']
    for i in range(count_mics):
        mics.append('Microphone ' + str(i + 1))
    mics.append('Add Microphone')

    buffer_removed = [0] * (len(mics) - 1)

    mic_opt = tkinter.StringVar()
    mic_opt.set("Select from list")
    mic_cb = ttk.Combobox(mic_win, width=20, height=60, textvariable=mic_opt)
    mic_cb['values'] = mics
    mic_cb.current(0)
    mic_cb['state'] = 'readonly'
    mic_cb.place(x=120, y=12)

    mic_cb.bind('<<ComboboxSelected>>', mic_option_change)

    def select_muted():
        if check_mute.get() == 1:
            check_mute_btn.select()
        else:
            check_mute_btn.deselect()

    def change_remove_btn_text():
        remove_btn['text'] = 'Removed'
        buffer_removed[mics.index(mic_opt.get())] = 1



    mute_label = Label(mic_win, text='Muted', font=6).place(x=110, y=165)
    current_mic_ind = buffer_mics.prev_obj_index
    if len(buffer_mics.data) == 0:
        check_mute = 0  # Muted=0 - means active / 1-means disactive
    else:
        check_mute.set(buffer_mics.data[current_mic_ind][3])
    check_mute_btn = Checkbutton(mic_win, variable=check_mute, onvalue=1, offvalue=0, command=select_muted)
    check_mute_btn.place(x=160, y=165 )


    bt_apply = tkinter.Button(mic_win, text='Apply', font=5, width=7,
                               height=1, command=get_values).place(x=515, y=160)
    bt_ok = tkinter.Button(mic_win, text='OK', font=5, width=5,
                               height=1, command=get_values_and_destroy).place(x=665, y=160)
    bt_cancel = tkinter.Button(mic_win, text='Cancel', font=5, width=6,
                               height=1, command=mic_win.destroy).place(x=595, y=160)
    remove_btn = tkinter.Button(mic_win, text='Remove', font=5, width=8, height=1,
                                command=change_remove_btn_text)
    remove_btn.place(x=15, y=160)

    bt_play = tkinter.Button(mic_win, text='Play', font=5, width=7, height=1,
                             command=play_mic).place(x=15, y=50)
    bt_stop = tkinter.Button(mic_win, text="Stop", font=5, width=6, height=1,
                             command=stop_play_mic).place(x=180, y=50)
    bt_pause = tkinter.Button(mic_win, text="Pause", font=5, width=7, height=1,
                             command=pause_unpause_mic)
    bt_pause.place(x=95, y=50)

    """"
    bt_play = tkinter.Label(mic_win, text='Play', font=1)
    bt_play.bind('<Button-1>', play_mic)
    bt_play.place(x=15, y=50)

    bt_stop = tkinter.Label(mic_win, text='Stop', font=1)
    bt_stop.bind('<Button-2>', stop_play_mic)
    bt_stop.place(x=65, y=50)

    bt_pause = tkinter.Label(mic_win, text='Pause', font=1)
    bt_pause.bind('<Button-3>', pause_mic)
    bt_pause.place(x=115, y=50)
             """""

    """""
    explorer_btn = tkinter.Label(source_win, text="Browse wav file", font=1)
    explorer_btn.bind('<Button-1>', browse_wavfile)
    """""

    mic_win.mainloop()


# Simulation top level window -------------------------------------------
def open_simulation_window():
    sim_win = Toplevel(root_window)
    sim_win.geometry('450x310')
    sim_win.title('Simulation parameters')

    def fill_entries():
        for i in range(len(arr_entries)):
            arr_entries[i].insert(END, Data['Simulation parameters'][i])

    fs_label = Label(sim_win, text='Sampling Frequency(fs)', font=6).place(x=30, y=20)
    fs_entry = tkinter.Entry(sim_win)
    fs_entry.place(x=235, y=25)
    max_order_label = Label(sim_win, text='Max order', font=6).place(x=30, y=50)
    order_entry = tkinter.Entry(sim_win)
    order_entry.place(x=235, y=55)
    rt_label = Label(sim_win, text='Reverberation time(RT60)', font=6).place(x=30, y=80)
    rt_entry = tkinter.Entry(sim_win)
    rt_entry.place(x=235, y=85)

    ref_mic__label = Label(sim_win, text='Reference microphone', font=6).place(x=30, y=170)
    mic_entry = tkinter.Entry(sim_win)
    mic_entry.place(x=235, y=170)
    snr_label = Label(sim_win, text='SNR', font=6).place(x=30, y=200)
    snr_entry = tkinter.Entry(sim_win)
    snr_entry.place(x=235, y=200)

    arr_entries = [fs_entry, order_entry, rt_entry, mic_entry, snr_entry]

    fill_entries()

    def select_air_abs():
        if check_value_air.get() == 1:
            check_button_air.select()
        else:
            check_button_air.deselect()
        print(check_value_air.get())

    def select_ray_tracing():
        if check_value_ray.get() == 1:
            check_button_ray.select()
        else:
            check_button_ray.deselect()
        print(check_value_ray.get())

    def get_simulation_values():
        for i in range(len(arr_entries)):
            Data['Simulation parameters'][i] = int(arr_entries[i].get())
        Data['Simulation parameters'][5] = check_value_air.get()
        Data['Simulation parameters'][6] = check_value_ray.get()
        plot_room()
        plot_sin_sound()
        sim_win.destroy()

    absorbtion_label = Label(sim_win, text='Air absorbtion', font=6).place(x=30, y=110)
    check_value_air = tkinter.IntVar()
    check_value_air.set(Data['Simulation parameters'][5])
    check_button_air = Checkbutton(sim_win, variable=check_value_air, onvalue=1, offvalue=0, command=select_air_abs)
    check_button_air.place(x=230, y=110)

    ray_label = Label(sim_win, text='Ray tracing', font=6).place(x=30, y=140)
    check_value_ray = tkinter.IntVar()
    check_value_ray.set(Data['Simulation parameters'][6])
    check_button_ray = Checkbutton(sim_win, variable=check_value_ray, onvalue=1, offvalue=0, command=select_ray_tracing)
    check_button_ray.place(x=230, y=140)

    bt_accept = tkinter.Button(sim_win, text='Accept', font=5, width=6,
                               height=1, command=get_simulation_values).place(x=365, y=270)
    bt_cancel = tkinter.Button(sim_win, text='Cancel', font=5, width=6,
                               height=1, command=sim_win.destroy).place(x=285, y=270)

    sim_win.mainloop()


file = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=file)
file.add_command(label='New FIle', command=None)
file.add_command(label='Open..', command=None)
file.add_command(label='Save', command=None)
file.add_separator()
file.add_command(label='Exit', command=root_window.destroy)

configs = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Configs', menu=configs)
configs.add_command(label='Room', command=open_room_window)
configs.add_command(label='Source', command=open_source_window)
configs.add_command(label='Microphone', command=open_microphone_window)
# configs.add_separator()
configs.add_command(label='Simulation parameters', command=open_simulation_window)

simulate = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Simulate', menu=simulate)
simulate.add_command(label='Settings', command=None)
simulate.add_command(label='Ran', command=None)
simulate.add_command(label='Stop', command=None)

# Edit menu and commands
edit = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit)
edit.add_command(label='Copy', command=None)
edit.add_command(label='Paste', command=None)
edit.add_command(label='Select', command=None)
edit.add_separator()
edit.add_command(label='Find..', command=None)

# HElp menu
help = tkinter.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Help', menu=help)
help.add_command(label='Simulation help', command=None)
help.add_command(label='Documentation', command=None)
help.add_command(label='About app', command=None)

root_window.config(menu=menubar)

"""""
sources_label = tkinter.LabelFrame(root_window, height=150, width=350, text='Sources')
sources_label.place(x=10, y=10)
source_canvas = tkinter.Canvas(sources_label,)

def open_source(s_index):
    open_source_window()
    source_opt.set(f'Source {s_index}')

def source_disactive(label, s_index):
    if label['text'] == 'Disactive':
        label['text'] = 'Active'
    else:
        label['text'] = 'Disactive'

def source_disactiveAll(label):
    if label['text'] == 'Disactive All':
        label['text'] = 'Active All'
    else:
        label['text'] = 'Disactive All'

for i in range(Data['Count Sources']):
    source_lab = tkinter.Label(root_window, text=f'Source {i+1}', font=2)
    source_lab.place(x=15, y=40+35*i)
    source_lab.bind("<Button-1>", lambda e: open_source(i+1))

    disactive_lab = tkinter.Label(root_window, text=f'Disactive', font=2)
    disactive_lab.place(x=145, y=40+35*i)
    disactive_lab.bind("<Button-1>", lambda e: source_disactive(disactive_lab, i+1))

    disactiveAll_lab = tkinter.Label(root_window, text=f'Disactive All', font=2)
    disactiveAll_lab.place(x=225, y=40+35*i)
    disactiveAll_lab.bind("<Button-1>", lambda e: source_disactiveAll(disactiveAll_lab))

"""""


def simulate():
    sim_room = create_new_simulation_room()
    sim_room.generate_image_sources()
    sim_room.compute_rir()
    sim_room.simulate()
    sim_room.room.mic_array.to_wav(project_path + "mic1.wav", norm=True, bitdepth=np.int16)
    #mic = scipy.io.wavfile.read(project_path + "mic1.wav")
    #audio = mic[1]
    plot_sin_mic()


bt_simulate = tkinter.Button(root_window, text='Simulate', font=10, width=9, height=1, command=simulate)
bt_simulate.place(x=800, y=10)


root_window.mainloop()