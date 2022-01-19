import sys
import time
import yaml
from Sim_room_classes import *
import numpy as np
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtGui, QtWidgets, QtCore
from Sim_room_classes import *
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pybind11_builtins as __pybind11_builtins
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLineEdit,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QAction,
    QPushButton,
    QComboBox,
    QCheckBox,
    QRadioButton,
)


class Room(QWidget):
    def __init__(self):
        super(Room, self).__init__()
        self.setGeometry(0, 0, 400, 400)

def create_sim_room():
    with open('buffer_data.yaml') as f:
        configs = yaml.load(f, Loader=FullLoader)

    room_confs = configs['Room']

    sim_room = simulation_room(length=room_confs['length'], width=room_confs['width'], height=room_confs['height'],
                                   fs=configs['Simulation parameters']['fs'],
                                   max_order=configs['Simulation parameters']['max_order'],
                                   air_absorption=configs['Simulation parameters']['air_absorbtion'],
                                   ray_tracing=configs['Simulation parameters']['ray_tracing'],
                                   sources=[], microphones=[])

    # create soundsource objects from all sources with functional or file form, resample, and add them to sim_room
    for source in configs['Sources']:
        if configs['Sources'][source]['form'] == 0:
            # get source parameters from loaded file, and create source objects
            # if form is functional , it will be object of class - source_func
            # if form is wav file , it will be object of class - source_wav
            s_confs = configs['Sources'][source]['functional_form']
            s_func = source_func(**s_confs)
            s = create_source_functional(s_func)
        else:
            s_confs = configs['Sources'][source]['wav file']
            s_file = source_wav(**s_confs)
            s = create_source_from_file(s_file)
        s.resampleaudio(newfs=sim_room.fs)
        sim_room.add_source(s)

    # make all sources of sim_room same size
    for i in range(len(sim_room.list_sources)):
        if i != 0:
            sim_room.list_sources[i].make_same_sizes(secondsource=sim_room.list_sources[i - 1])

        """""
        if configs['Sources']['Source1']['form'] == 0:
            s1_confs = configs['Sources']['Source1']['functional_form']
            s1_func = source_func(**s1_confs)
            source1 = create_source_functional(s1_func)
        else:
            s1_confs = configs['Sources']['Source1']['wav file']
            s1_file = source_func(**s1_confs)
            source1 = create_source_from_file(s1_file)

        if configs['Sources']['Source2']['form'] == 0:
            s2_confs = configs['Sources']['Source2']['functional_form']
            s2_func = source_func(**s2_confs)
            source2 = create_source_functional(s2_func)
        else:
            s2_confs = configs['Sources']['Source2']['wav file']
            s2_file = source_wav(**s2_confs)
            source2 = create_source_from_file(s2_file)

        source1.resampleaudio(newfs=sim_room.fs)
        source2.resampleaudio(newfs=sim_room.fs)
        source2.make_same_sizes(secondsource=source1)

        sim_room.add_source(source1)
        sim_room.add_source(source2)
        """""

    # create microphone objects from all microphones and add them to sim_room
    for mic in configs['microphones']:
        mic_confs = configs['microphones'][mic]
        m = microphone(**mic_confs)
        sim_room.add_microphone(m)

    return sim_room

def create_room_graphics():
    sim_room = create_sim_room()
    return Room_gui(walls=[], sources=sim_room.list_sources, mics=sim_room.list_microphones)


class _Widget(QtWidgets.QWidget):
    def __init__(self):
        super(_Widget, self).__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.room = create_sim_room()
        self.room_graphic = Room_gui(walls=[], sources=self.room, mics=self.room.list_microphones)
        self.fig_room, self.ax = self.room_graphic.plot(mic_marker_size=30, figsize=(5, 3))
        self.ax.set_xlim([0, self.room.room_dim[0] + 5])
        self.ax.set_ylim([0, self.room.room_dim[1] + 5])
        self.ax.set_zlim([0, self.room.room_dim[2] + 5])

        canvas = FigureCanvas(self.fig_room)
        toolbar = NavigationToolbar(canvas, self)

        layout.addWidget(toolbar)
        layout.addWidget(canvas)

    """""
    def _update_canvas(self):
        self.room = create_sim_room()
        self.fig_room.set_data(self.room.room)

        self.fig_room.figure.canvas.draw()
    """""


class CanvasWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CanvasWidget, self).__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = _Widget()
        self.layout.addWidget(self.canvas)

    def update(self):
        self.layout.removeWidget(self.canvas)
        self.canvas = _Widget()
        self.layout.addWidget(self.canvas)


# the main window, that appears on screen just after running app
class MainWindow(QMainWindow):
    def __init__(self):
        # parent QMainWindow constructor
        super(MainWindow, self).__init__()

        self.setWindowTitle('My app')
        geometry = app.desktop().availableGeometry()
        self.setGeometry(geometry)

        self.source_window = SourceWindow(parent=self)
        self.microphone_window = MicrophoneWindow(parent=self)
        self.room_window = RoomWindow(parent=self)
        self.sim_parameters_window = SimulationParametersWindow()

        # the main horizontal layout that shares the screen into 2 parts
        self.layout = QHBoxLayout()
        # left side vertical layout, where should be  widgets for source, microphone and player
        self.layout_left = QVBoxLayout()
        # right side vertical layout, where should be plots for room, sound and mic waveforms
        self.layout_right = QVBoxLayout()

        # plotting room
        #self.room = Room()
        #self.plot_room(self.room)

        # room canvas
        self.canvas = CanvasWidget()
        self.layout_right.setContentsMargins(0, 0, 0, 0)
        self.layout_right.addWidget(self.canvas)
        #self.layout_right.addWidget(self.button)
       # self.button.clicked.connect(self.update_)

        # adding room plot to its layout
        #self.layout_right.addWidget(self.toolbar)
        #self.layout_right.addWidget(self.canvas)

        self.layout.addLayout(self.layout_left)
        self.layout.addLayout(self.layout_right)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        # Menu bar
        # File
        newfile_action = QAction("New File", self)
        newfile_action.triggered.connect(self.onMenuBarFileClick)
        open_action = QAction("Open..", self)
        open_action.triggered.connect(self.onMenuBarFileClick)
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.onMenuBarFileClick)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.onMenuBarFileClick)

        # Configs
        room_action = QAction("Room", self)
        room_action.triggered.connect(self.show_Room_window)
        source_action = QAction("Source", self)
        source_action.triggered.connect(self.show_Sources_window)
        mic_action = QAction("Microphone", self)
        mic_action.triggered.connect(self.show_Microphones_window)
        simparams_action = QAction("Simulation parameters", self)
        simparams_action.triggered.connect(self.show_Sim_parameters_window)

        # Simulate
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.onMenuBarFileClick)
        run_action = QAction("Run", self)
        run_action.triggered.connect(self.run_simulation)
        stop_action = QAction("Stop", self)
        stop_action.triggered.connect(self.onMenuBarFileClick)

        # Edit
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.onMenuBarFileClick)
        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.onMenuBarFileClick)
        select_action = QAction("Select", self)
        select_action.triggered.connect(self.onMenuBarFileClick)
        find_action = QAction("Find", self)
        find_action.triggered.connect(self.onMenuBarFileClick)

        # Help
        simhelp_action = QAction("Simulation help", self)
        simhelp_action.triggered.connect(self.onMenuBarFileClick)
        doc_action = QAction("Documantation", self)
        doc_action.triggered.connect(self.onMenuBarFileClick)
        aboutApp_action = QAction("About app", self)
        aboutApp_action.triggered.connect(self.onMenuBarFileClick)

        menu = self.menuBar()
        file_menu = menu.addMenu("File")
        file_menu.addAction(newfile_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        configs_menu = menu.addMenu("Configs")
        configs_menu.addAction(room_action)
        configs_menu.addAction(source_action)
        configs_menu.addAction(mic_action)
        configs_menu.addAction(simparams_action)

        simulate_menu = menu.addMenu("Simulate")
        simulate_menu.addAction(settings_action)
        simulate_menu.addAction(run_action)
        simulate_menu.addAction(stop_action)

        edit_menu = menu.addMenu("Edit")
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addAction(select_action)
        edit_menu.addAction(copy_action)
        edit_menu.addSeparator()
        edit_menu.addAction(find_action)

        help_menu = menu.addMenu("Help")
        help_menu.addAction(simhelp_action)
        help_menu.addAction(doc_action)
        help_menu.addAction(aboutApp_action)

    def onMenuBarFileClick(self, status):
        print(status)

    # functions for display config windows - Room, Source, Microphones,

    # Simulation parameters
    def show_Sources_window(self):
        if self.source_window.isVisible():
            self.source_window.hide()
        else:
            self.source_window.show()

    def show_Microphones_window(self):
        if self.microphone_window.isVisible():
            self.microphone_window.hide()
        else:
            self.microphone_window.show()

    def show_Room_window(self):
        if self.room_window.isVisible():
            self.room_window.hide()
        else:
            self.room_window.show()

    def show_Sim_parameters_window(self):
        if self.sim_parameters_window.isVisible():
            self.sim_parameters_window.hide()
        else:
            self.sim_parameters_window.show()

    def update_(self):
        self.canvas.update()


    def run_simulation(self):
        sim_room = self.create_sim_room()
        sim_room.generate_image_sources()
        sim_room.compute_rir()
        sim_room.simulate()
        # save sound of microphone in a wav file
        sim_room.room.mic_array.to_wav("D:\\Simulation results\\mic1.wav", norm=True, bitdepth=np.int16)

    """""
    def plot_room(self, target_widget):

        room = self.create_sim_room()
        self.fig_room, self.ax = room.room.plot(mic_marker_size=30, figsize=(6, 3.5))

        self.ax.set_xlim([0, room.room_dim[0] + 5])
        self.ax.set_ylim([0, room.room_dim[1] + 5])
        self.ax.set_zlim([0, room.room_dim[2] + 5])

        self.canvas = FigureCanvas(self.fig_room)
        self.toolbar = NavigationToolbar(self.canvas, target_widget)

        self.canvas.draw()
    """""


class SourceWindow(QWidget):
    def __init__(self, parent=None):
        super(SourceWindow, self).__init__()
        self.setWindowTitle("Sources")
        self.setGeometry(150, 80, 450, 420)
        self.parent = parent

        """""
        with open('Initial_configs.yaml') as f:
            data = yaml.load(f, Loader=FullLoader)
        self.source_configs = data['Sources']
        """""

        with open('buffer_data.yaml') as f:
            self.buffer = yaml.load(f, Loader=FullLoader)['Sources']

        # main layout with column and rows
        self.layout = QGridLayout()
        # layout for select source,  mute/remove, functional/wav file
        self.layout1 = QGridLayout()
        # layout for functional or wav file widgets
        self.layout_form = QGridLayout()
        # layout for apply/cancel/ok buttons
        self.layout5 = QHBoxLayout()

        # layout1 - layout for select source,  mute/remove, functional/wav file
        # create widget, for select source
        self.sources = QComboBox()
        self.sources.setEditable(True)  # to add sources
        for i in range(len(self.buffer)):
            self.sources.addItem('Source' + str(i + 1))
        self.sources.addItem("Add Source")

        self.mute_box = QCheckBox("Mute")
        self.mute_box.setCheckable(True)
        self.rmmove_box = QCheckBox("Remove")
        self.rmmove_box.setCheckable(True)

        # create entry-widgets for input x, y, z coordinates
        self.x_pos_line_edit = QLineEdit()
        self.x_pos_line_edit.setPlaceholderText("X coordinate")
        self.y_pos_line_edit = QLineEdit()
        self.y_pos_line_edit.setPlaceholderText("Y coordinate")
        self.z_pos_line_edit = QLineEdit()
        self.z_pos_line_edit.setPlaceholderText("Z coordinate")
        # create widgets for select source form - functional or wav file
        self.func_radiobtn = QRadioButton("Functional")
        self.file_radiobtn = QRadioButton("Wav file")

        # adding created widgets to layout
        self.layout1.addWidget(self.sources, 0, 0)
        self.layout1.addWidget(self.mute_box, 0, 2)
        self.layout1.addWidget(self.rmmove_box, 0, 3)
        self.layout1.addWidget(self.func_radiobtn, 1, 0)
        self.layout1.addWidget(self.file_radiobtn, 1, 1)
        self.layout1.addWidget(QLabel("Position"), 2, 0)
        self.layout1.addWidget(self.x_pos_line_edit, 2, 1)
        self.layout1.addWidget(self.y_pos_line_edit, 2, 2)
        self.layout1.addWidget(self.z_pos_line_edit, 2, 3)

        # create func form widgets
        self.amp_line_edit = QLineEdit()
        self.amp_line_edit.setPlaceholderText("Amplitude")
        self.freq_line_edit = QLineEdit()
        self.freq_line_edit.setPlaceholderText("Frequency")
        self.fs_line_edit_ = QLineEdit()
        self.fs_line_edit_.setPlaceholderText("Sampling frequency")
        self.phase_line_edit = QLineEdit()
        self.phase_line_edit.setPlaceholderText("Phase")
        self.time_line_edit = QLineEdit()
        self.time_line_edit.setPlaceholderText("Duration")

        self.amp_label = QLabel("Amplitude")
        self.freq_label = QLabel("Frequency")
        self.fs_label_ = QLabel("Sampling freqyuency")
        self.phase_label = QLabel("Phase")
        self.time_label = QLabel("Time")

        # list of functional form widgets
        self.func_widgets = [self.amp_label, self.amp_line_edit, self.freq_label, self.freq_line_edit, self.fs_label_,
                             self.fs_line_edit_, self.phase_label, self.phase_line_edit, self.time_label,
                             self.time_line_edit]

        # create file form widgets
        self.browse_btn = QPushButton('Browse .wav file')
        self.file_lineedit = QLineEdit()
        self.t_start_label = QLabel("T start")
        self.t_end_label = QLabel('T end')
        self.t_label = QLabel('Time')
        self.tstart_lineedit = QLineEdit()
        self.tend_lineedit = QLineEdit()
        self.t_lineedit = QLineEdit()
        self.fs_label = QLabel('Fs')
        self.fs_lineedit = QLineEdit()

        self.file_widgets = [self.browse_btn, self.file_lineedit, self.t_start_label, self.t_end_label, self.fs_label,
                             self.tstart_lineedit, self.tend_lineedit, self.t_lineedit, self.fs_lineedit,
                             self.t_label]

        # create apply/cancel/ok buttons
        self.btn_ok = QPushButton("OK")
        self.btn_ok.setStyleSheet("color: white;")
        self.btn_ok.setStyleSheet("Background-color: grey;")
        self.btn_apply = QPushButton("Apply")
        self.btn_apply.setStyleSheet("Background-color: grey;")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("Background-color: grey;")

        self.layout5.addWidget(self.btn_apply)
        self.layout5.addWidget(self.btn_cancel)
        self.layout5.addWidget(self.btn_ok)

        # after creating al widgets, initialize them with buffer values
        self.initialize_source_window()
        self.filling_entries('Source1')

        # source change operation connect to source_changed method
        self.sources.currentTextChanged.connect(self.source_changed)
        # QComboBox.InsertBeforeCurrent- insert will be handled like this -
        # Insert before current item(before add source item) - for adding source
        self.sources.setInsertPolicy(QComboBox.InsertBeforeCurrent)

        # function/wav file selection connect to-
        # to_functional method for functional form and
        # to_wav_file method for wav file form
        # same for mute/ remove checkboxes, and browse button and etc
        self.func_radiobtn.toggled.connect(self.to_functional)
        self.file_radiobtn.toggled.connect(self.to_wav_file)
        self.mute_box.stateChanged.connect(self.change_mute_state)
        self.rmmove_box.stateChanged.connect(self.change_remove_state)
        self.browse_btn.clicked.connect(self.browse_file)

        self.amp_line_edit.textChanged.connect(self.get_amplitude)
        self.freq_line_edit.textChanged.connect(self.get_frequency)
        self.fs_line_edit_.textChanged.connect(self.get_fs_func)
        self.phase_line_edit.textChanged.connect(self.get_phase)
        self.time_line_edit.textChanged.connect(self.get_time_func)
        self.file_lineedit.textChanged.connect(self.get_file)
        self.tstart_lineedit.textChanged.connect(self.get_start_time)
        self.tend_lineedit.textChanged.connect(self.get_end_time)
        self.t_lineedit.textChanged.connect(self.get_time_fileform)
        self.fs_lineedit.textChanged.connect(self.get_fs_fileform)

        self.x_pos_line_edit.textChanged.connect(self.get_x)
        self.y_pos_line_edit.textChanged.connect(self.get_y)
        self.z_pos_line_edit.textChanged.connect(self.get_z)

        self.btn_ok.clicked.connect(self.push_parameters_to_data_and_destroy)
        self.btn_apply.clicked.connect(self.refresh_parameters)
        self.btn_cancel.clicked.connect(self.hide)

        self.layout.addLayout(self.layout1, 0, 0)
        self.layout.addLayout(self.layout_form, 1, 0)
        self.layout.addLayout(self.layout5, 2, 0)
        self.setLayout(self.layout)

    # methods connected with widgets
    def get_amplitude(self, amplitude: str):
        source = str(self.sources.currentText())
        if amplitude == "":
            amplitude = 0
        self.buffer[source]['functional_form']['amplitude'] = int(amplitude)

    def get_frequency(self, freq: str):
        source = str(self.sources.currentText())
        if freq == "":
            freq = 0
        self.buffer[source]['functional_form']['frequency'] = int(freq)

    def get_fs_func(self, fs: str):
        source = str(self.sources.currentText())
        if fs == "":
            fs = 0
        self.buffer[source]['functional_form']['fs'] = int(fs)

    def get_phase(self, phase: str):
        source = str(self.sources.currentText())
        if phase == "":
            phase = 0
        self.buffer[source]['functional_form']['phase'] = int(phase)

    def get_time_func(self, time: str):
        source = str(self.sources.currentText())
        if time == "":
            time = 0
        self.buffer[source]['functional_form']['time'] = int(time)

    # ---- file form ---
    def get_file(self, file: str):
        source = str(self.sources.currentText())
        if file == "":
            file = " "
        self.buffer[source]['wav file']['filename'] = file

    def get_start_time(self, stime: str):
        source = str(self.sources.currentText())
        if stime == "":
            stime = 0
        self.buffer[source]['wav file']['t_start'] = int(stime)

    def get_end_time(self, etime: str):
        source = str(self.sources.currentText())
        if etime == "":
            etime = 0
        self.buffer[source]['wav file']['t_end'] = int(etime)

    def get_time_fileform(self, time: str):
        source = str(self.sources.currentText())
        if time == "":
            time = 0
        self.buffer[source]['wav file']['time'] = float(time)

    def get_fs_fileform(self, fs: str):
        source = str(self.sources.currentText())
        if fs == "":
            fs = 0
        self.buffer[source]['wav file']['fs'] = int(fs)

    def get_x(self, x: str):
        source = str(self.sources.currentText())
        if x == "":
            x = 0
        self.buffer[source]['wav file']['x'] = int(x)
        self.buffer[source]['functional_form']['x'] = int(x)

    def get_y(self, y: str):
        source = str(self.sources.currentText())
        if y == "":
            y = 0
        self.buffer[source]['wav file']['y'] = int(y)
        self.buffer[source]['functional_form']['y'] = int(y)

    def get_z(self, z: str):
        source = str(self.sources.currentText())
        if z == "":
            z = 0
        self.buffer[source]['wav file']['z'] = int(z)
        self.buffer[source]['functional_form']['z'] = int(z)

    def source_index_changed(self, index):
        print("Source", index)

    def source_changed(self, s: str):
        if s != 'Add Source':
            self.filling_entries(s)

    def to_functional(self, selected):
        if selected:
            for i in range(len(self.file_widgets)):
                self.file_widgets[i].hide()
            for i in range(len(self.func_widgets)):
                self.func_widgets[i].show()

            source = str(self.sources.currentText())
            self.buffer[source]['form'] = 0  # source is functional form(0-func form)

    def to_wav_file(self, selected):
        if selected:
            for i in range(len(self.func_widgets)):
                self.func_widgets[i].hide()
            for i in range(len(self.file_widgets)):
                self.file_widgets[i].show()
            source = str(self.sources.currentText())
            self.buffer[source]['form'] = 1  # source is wav form(1-file form)

    def browse_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*.wav')
        self.file_lineedit.setText(filename)

    def change_mute_state(self, state):
        if state == True:
            print(state)  # tesnel vor sourcena comboboxum, u ira bufferi muted=1 dnel

    def change_remove_state(self, state):
        if state == True:
            print(state)  # tesnel vor sourcena comboboxum, u iran remove anel

    def initialize_source_window(self):
        self.layout_form.addWidget(self.amp_label, 0, 0)
        self.layout_form.addWidget(self.amp_line_edit, 0, 1)
        self.layout_form.addWidget(self.freq_label, 1, 0)
        self.layout_form.addWidget(self.freq_line_edit, 1, 1)
        self.layout_form.addWidget(self.fs_label_, 2, 0)
        self.layout_form.addWidget(self.fs_line_edit_, 2, 1)
        self.layout_form.addWidget(self.phase_label, 0, 2)
        self.layout_form.addWidget(self.phase_line_edit, 0, 3)
        self.layout_form.addWidget(self.time_label, 1, 2)
        self.layout_form.addWidget(self.time_line_edit, 1, 3)

        self.layout_form.addWidget(self.browse_btn, 0, 0)
        self.layout_form.addWidget(self.file_lineedit, 0, 1)
        self.layout_form.addWidget(self.t_start_label, 1, 0)
        self.layout_form.addWidget(self.tstart_lineedit, 1, 1)
        self.layout_form.addWidget(self.t_end_label, 1, 2)
        self.layout_form.addWidget(self.tend_lineedit, 1, 3)
        self.layout_form.addWidget(self.t_label, 1, 4)
        self.layout_form.addWidget(self.t_lineedit, 1, 5)
        self.layout_form.addWidget(self.fs_label, 2, 0)
        self.layout_form.addWidget(self.fs_lineedit, 2, 1)

        for i in range(len(self.file_widgets)):
            self.file_widgets[i].hide()

        for i in range(len(self.func_widgets)):
            self.func_widgets[i].hide()

    def filling_entries(self, s: str):
        # if self.source_configs[s]['muted'] == 0:
        self.func_s = self.buffer[s]['functional_form']
        self.file_s = self.buffer[s]['wav file']

        self.x_pos_line_edit.setText(str(self.func_s['x']))
        self.y_pos_line_edit.setText(str(self.func_s['y']))
        self.z_pos_line_edit.setText(str(self.func_s['z']))

        if self.buffer[s]['form'] == 0:  # functional form
            self.func_radiobtn.setChecked(True)
            self.to_functional(True)
            self.file_radiobtn.setChecked(False)
        else:  # file form
            self.file_radiobtn.setChecked(True)
            self.to_wav_file(True)
            self.func_radiobtn.setChecked(False)

        self.amp_line_edit.setText(str(self.func_s['amplitude']))
        self.fs_line_edit_.setText(str(self.func_s['fs']))
        self.freq_line_edit.setText(str(self.func_s['frequency']))
        self.phase_line_edit.setText(str(self.func_s['phase']))
        self.time_line_edit.setText(str(self.func_s['time']))

        self.file_lineedit.setText(self.file_s['filename'])
        self.tstart_lineedit.setText(str(self.file_s['t_start']))
        self.tend_lineedit.setText(str(self.file_s['t_end']))
        self.t_lineedit.setText(str(self.file_s['time']))
        self.fs_lineedit.setText(str(self.file_s['fs']))

    # connected to ok button, for pushing values to main data, and hide window
    def push_parameters_to_data_and_destroy(self):
        self.refresh_parameters()

        with open('Data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
        d['Sources'] = self.buffer
        with open('Data.yaml', 'w') as f:
            yaml.dump(d, f)

        self.hide()

    # connected to apply button, for updating buffer data
    def refresh_parameters(self):
        with open('buffer_data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
        d['Sources'] = self.buffer
        with open('buffer_data.yaml', 'w') as f:
            yaml.dump(d, f)

        if self.parent:
            self.parent.update_()


class MicrophoneWindow(QWidget):
    def __init__(self, parent=None):
        super(MicrophoneWindow, self).__init__()
        self.setWindowTitle("Microphones")
        self.setGeometry(150, 80, 550, 250)
        self.parent = parent

        """""
        with open('Initial_configs.yaml') as f:
            data = yaml.load(f, Loader=FullLoader)
        self.mic_configs = data['microphones']
        """""

        with open('buffer_data.yaml') as f:
            self.buffer = yaml.load(f, Loader=FullLoader)['microphones']

        # main vertical layout
        layout = QVBoxLayout()
        # layout for selecting mic, its coordinates, mute/remove,  play, stop, pause
        layout1 = QGridLayout()
        # layout for apply/cancel/ok buttons
        layout3 = QHBoxLayout()

        # select microphone
        self.microphones = QComboBox()
        self.microphones.setEditable(True)  # to add sources
        self.microphones.addItems(["Microphone1", "Microphone2" "Add Microphone"])

        # self.microphones.currentIndexChanged.connect(self.microphone_index_changed)
        # mic selection connect to mic_changed method
        self.microphones.currentTextChanged.connect(self.mic_changed)
        # QComboBox.InsertBeforeCurrent- insert will be handled like this -
        # Insert before current item(before add source item) - for adding mic
        self.microphones.setInsertPolicy(QComboBox.InsertBeforeCurrent)

        # create widgets
        self.mute_box = QCheckBox("Mute")
        self.mute_box.setCheckable(True)
        self.mute_box.stateChanged.connect(self.show_state)
        self.rmmove_box = QCheckBox("Remove")
        self.rmmove_box.setCheckable(True)
        self.rmmove_box.stateChanged.connect(self.show_state)

        self.position_label = QLabel("Position")
        self.x_pos_line_edit = QLineEdit()
        self.x_pos_line_edit.setPlaceholderText("X coordinate")
        self.y_pos_line_edit = QLineEdit()
        self.y_pos_line_edit.setPlaceholderText("Y coordinate")
        self.z_pos_line_edit = QLineEdit()
        self.z_pos_line_edit.setPlaceholderText("Z coordinate")

        # add widgets to first layout
        layout1.addWidget(self.microphones, 0, 0)
        layout1.addWidget(self.mute_box, 0, 2)
        layout1.addWidget(self.rmmove_box, 0, 3)
        layout1.addWidget(self.position_label, 1, 0)
        layout1.addWidget(self.x_pos_line_edit, 1, 1)
        layout1.addWidget(self.y_pos_line_edit, 1, 2)
        layout1.addWidget(self.z_pos_line_edit, 1, 3)

        layout2 = QHBoxLayout()

        self.play_btn = QPushButton("Play")
        self.pause_btn = QPushButton("Pause")
        self.stop_btn = QPushButton("Stop")
        self.filepath_line_edit = QLineEdit()
        # self.filepath_line_edit.setPlaceholderText("file path")
        self.filepath_line_edit.setText("C:\pyqtSimulation results\mic1.wav")

        layout2.addWidget(self.play_btn)
        layout2.addWidget(self.pause_btn)
        layout2.addWidget(self.stop_btn)
        layout2.addWidget(self.filepath_line_edit)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setStyleSheet("color: white;")
        self.btn_ok.setStyleSheet("Background-color: grey;")
        self.btn_apply = QPushButton("Apply")
        self.btn_apply.setStyleSheet("Background-color: grey;")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("Background-color: grey;")

        # initialize entries with buffer values for Microphone1
        self.filling_entries('Microphone1')

        # connect widgets with methods
        self.x_pos_line_edit.textChanged.connect(self.get_x)
        self.y_pos_line_edit.textChanged.connect(self.get_y)
        self.z_pos_line_edit.textChanged.connect(self.get_z)

        self.btn_apply.clicked.connect(self.refresh_parameters)
        self.btn_ok.clicked.connect(self.push_parameters_to_data_and_destroy)
        self.btn_cancel.clicked.connect(self.hide)

        layout3.addWidget(self.btn_apply)
        layout3.addWidget(self.btn_cancel)
        layout3.addWidget(self.btn_ok)

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        self.setLayout(layout)

    def filling_entries(self, m: str):
        self.x_pos_line_edit.clear()
        self.y_pos_line_edit.clear()
        self.z_pos_line_edit.clear()

        self.x_pos_line_edit.setText(str(self.buffer[m]['x']))
        self.y_pos_line_edit.setText(str(self.buffer[m]['y']))
        self.z_pos_line_edit.setText(str(self.buffer[m]['z']))

    # method for taking tha value of x coordinate from entry, and save it in buffer
    def get_x(self, x: str):
        mic = str(self.microphones.currentText())
        if x == "":
            x = 0

        self.buffer[mic]['x'] = int(x)

    def get_y(self, y: str):
        mic = str(self.microphones.currentText())
        if y == "":
            y = 0

        self.buffer[mic]['y'] = int(y)

    def get_z(self, z: str):
        mic = str(self.microphones.currentText())
        if z == "":
            z = 0

        self.buffer[mic]['z'] = int(z)

    # push values to main data and hide the window/ is connected to ok button
    def push_parameters_to_data_and_destroy(self):
        self.refresh_parameters()

        with open('Data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
        d['microphones'] = self.buffer
        with open('Data.yaml', 'w') as f:
            yaml.dump(d, f)

        self.hide()

    # push values to buffer / is connected to apply button
    def refresh_parameters(self):
        with open('buffer_data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
        d['microphones'] = self.buffer
        with open('buffer_data.yaml', 'w') as f:
            yaml.dump(d, f)

        if self.parent:
            self.parent.update_()

    # this method is not used still
    def microphone_index_changed(self, index):
        print("Microphone", index)

    def mic_changed(self, m: str):
        if m != 'Add Microphone':
            self.filling_entries(m)

    def show_state(self, state):
        print(state == Qt.Checked)
        print(state)


class RoomWindow(QWidget):
    def __init__(self, parent=None):
        super(RoomWindow, self).__init__()
        self.setWindowTitle("Room")
        self.setGeometry(150, 80, 350, 400)
        self.parent = parent

        with open('buffer_data.yaml') as f:
            self.data = yaml.load(f, Loader=FullLoader)
        self.room_configs = self.data['Room']

        # main layout
        layout = QVBoxLayout()
        # layout for room sizes and environment parameters
        layout1 = QGridLayout()
        # layout for apply/cancel/ok buttons
        layout2 = QHBoxLayout()

        # create entriy-widgets of room sizes and environment parameter
        self.length_lineedit = QLineEdit()
        self.width_lineedit = QLineEdit()
        self.height_lineedit = QLineEdit()
        self.temp_lineedit = QLineEdit()
        self.humadity_lineedit = QLineEdit()

        # add widgets to layout
        layout1.addWidget(QLabel("Sizes"), 0, 0)
        layout1.addWidget(QLabel("Length"), 1, 0)
        layout1.addWidget(QLabel("Width"), 2, 0)
        layout1.addWidget(QLabel("Height"), 3, 0)
        layout1.addWidget(QLabel("Environment"), 4, 0)
        layout1.addWidget(QLabel("Temperature"), 5, 0)
        layout1.addWidget(QLabel("Humadity"), 6, 0)

        layout1.addWidget(self.length_lineedit, 1, 1)
        layout1.addWidget(self.width_lineedit, 2, 1)
        layout1.addWidget(self.height_lineedit, 3, 1)
        layout1.addWidget(self.temp_lineedit, 5, 1)
        layout1.addWidget(self.humadity_lineedit, 6, 1)

        # combobox of materials for walls and floor to select
        self.walls = QComboBox()
        self.walls.setEditable(False)
        self.floor = QComboBox()
        self.floor.setEditable(False)

        layout1.addWidget(QLabel("Surface materials"), 7, 0)
        layout1.addWidget(QLabel("Walls"), 8, 0)
        layout1.addWidget(self.walls, 8, 1)

        layout1.addWidget(QLabel("Floor"), 9, 0)
        layout1.addWidget(self.floor, 9, 1)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setStyleSheet("color: white;")
        self.btn_ok.setStyleSheet("Background-color: grey;")

        self.btn_apply = QPushButton("Apply")
        self.btn_apply.setStyleSheet("Background-color: grey;")

        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("Background-color: grey;")

        layout2.addWidget(self.btn_apply)
        layout2.addWidget(self.btn_cancel)
        layout2.addWidget(self.btn_ok)

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        self.setLayout(layout)

        self.initialize_entries()

        self.length_lineedit.textChanged.connect(self.change_length)
        self.width_lineedit.textChanged.connect(self.change_width)
        self.height_lineedit.textChanged.connect(self.change_height)
        self.temp_lineedit.textChanged.connect(self.change_temperature)
        self.humadity_lineedit.textChanged.connect(self.change_humadity)
        self.walls.currentTextChanged.connect(self.wall_material_changed)
        self.floor.currentTextChanged.connect(self.floor_material_changed)
        self.btn_ok.clicked.connect(self.push_parameters_to_data_and_destroy)
        self.btn_apply.clicked.connect(self.refresh_parameters)
        self.btn_cancel.clicked.connect(self.hide)

    # initialzing widgets with data values
    def initialize_entries(self):
        self.walls.addItems(self.data['Material values'])
        self.floor.addItems(self.data['Material values'])

        self.walls.setCurrentIndex(self.room_configs['walls'])
        self.floor.setCurrentIndex(self.room_configs['floor'])
        self.length_lineedit.setText(str(self.room_configs['length']))
        self.width_lineedit.setText(str(self.room_configs['width']))
        self.height_lineedit.setText(str(self.room_configs['height']))
        self.temp_lineedit.setText(str(self.room_configs['temperature']))
        self.humadity_lineedit.setText(str(self.room_configs['humadity']))

    # methods connected with appropriate widgets
    # this one for room length input
    def change_length(self, l):
        self.room_configs['length'] = int(l)

    def change_width(self, w):
        self.room_configs['width'] = int(w)

    def change_height(self, h):
        self.room_configs['height'] = int(h)

    def change_temperature(self, t):
        self.room_configs['temperature'] = int(t)

    def change_humadity(self, h):
        self.room_configs['humadity'] = int(h)

    # methods connected with walls and floor comboboxes, to select material
    def wall_material_changed(self, material_ind):
        self.walls.setCurrentIndex(self.data['Material values'].index(material_ind))
        self.room_configs['walls'] = self.data['Material values'].index(material_ind)

    def floor_material_changed(self, material_ind):
        self.floor.setCurrentIndex(self.data['Material values'].index(material_ind))
        self.room_configs['Room']['floor'] = self.data['Material values'].index(material_ind)

    # send values to data and hide window/ connected to okbuttond
    def push_parameters_to_data_and_destroy(self):
        self.refresh_parameters()
        with open('Data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
        d['Room'] = self.room_configs
        with open('Data.yaml', 'w') as f:
            yaml.dump(d, f)

        self.hide()

    def refresh_parameters(self):
        with open('buffer_data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
            d['Room'] = self.room_configs
        with open('buffer_data.yaml', 'w') as f:
            yaml.dump(d, f, sort_keys=False, indent=4)

        if self.parent:
            self.parent.update_()


class SimulationParametersWindow(QWidget):
    def __init__(self):
        super(SimulationParametersWindow, self).__init__()
        self.setWindowTitle("Simulation parameters")
        self.setGeometry(150, 80, 350, 350)

        with open('Initial_configs.yaml') as f:
            self.data = yaml.load(f, Loader=FullLoader)
        self.sim_configs = self.data['Simulation parameters']

        layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout2 = QHBoxLayout()

        self.fs_lineedit = QLineEdit()
        self.max_order_lineedit = QLineEdit()
        self.rt60_lineedit = QLineEdit()
        self.absorbtion = QCheckBox()
        self.absorbtion.setCheckable(True)
        self.ray_tracing = QCheckBox()
        self.ray_tracing.setCheckable(True)
        self.ref_mic_lineedit = QLineEdit()
        self.snr_lineedit = QLineEdit()

        layout1.addWidget(QLabel("Sampling frequency"), 0, 0)
        layout1.addWidget(self.fs_lineedit, 0, 1)
        layout1.addWidget(QLabel("Max order"), 1, 0)
        layout1.addWidget(self.max_order_lineedit, 1, 1)
        layout1.addWidget(QLabel("Reverberation time (RT60)"), 2, 0)
        layout1.addWidget(self.rt60_lineedit, 2, 1)
        layout1.addWidget(QLabel("Reference microphone"), 3, 0)
        layout1.addWidget(self.ref_mic_lineedit, 3, 1)
        layout1.addWidget(QLabel("SNR"), 4, 0)
        layout1.addWidget(self.snr_lineedit, 4, 1)
        layout1.addWidget(QLabel("Air absorbtion"), 5, 0)
        layout1.addWidget(self.absorbtion, 5, 1)
        layout1.addWidget(QLabel("Ray tracing"), 6, 0)
        layout1.addWidget(self.ray_tracing, 6, 1)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setStyleSheet("color: white;")
        self.btn_ok.setStyleSheet("Background-color: grey;")
        self.btn_apply = QPushButton("Apply")
        self.btn_apply.setStyleSheet("Background-color: grey;")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("Background-color: grey;")

        layout2.addWidget(self.btn_apply)
        layout2.addWidget(self.btn_cancel)
        layout2.addWidget(self.btn_ok)

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        self.setLayout(layout)

        self.initialize_entries()

        self.fs_lineedit.textChanged.connect(self.change_fs)
        self.max_order_lineedit.textChanged.connect(self.change_max_order)
        self.rt60_lineedit.textChanged.connect(self.change_reverberation_time)
        self.absorbtion.stateChanged.connect(self.change_absorbtion)
        self.ray_tracing.stateChanged.connect(self.change_ray_tracing)
        self.ref_mic_lineedit.textChanged.connect(self.change_reference_mic)
        self.snr_lineedit.textChanged.connect(self.change_snr)
        self.btn_ok.clicked.connect(self.load_parameters_to_data_and_destroy)
        self.btn_apply.clicked.connect(self.load_parameters_to_data)
        self.btn_cancel.clicked.connect(self.hide)

    def initialize_entries(self):
        self.fs_lineedit.setText(str(self.sim_configs['fs']))
        self.max_order_lineedit.setText(str(self.sim_configs['max_order']))
        self.rt60_lineedit.setText(str(self.sim_configs['reverberation_time']))
        self.absorbtion.setChecked(self.sim_configs['air_absorbtion'])
        self.ray_tracing.setChecked(self.sim_configs['ray_tracing'])
        self.ref_mic_lineedit.setText(str(self.sim_configs['reference_microphone']))
        self.snr_lineedit.setText(str(self.sim_configs['SNR']))

    def change_fs(self, f):
        self.sim_configs['fs'] = int(f)

    def change_max_order(self, mo):
        self.sim_configs['max_order'] = int(mo)

    def change_reverberation_time(self, rt):
        self.sim_configs['reverberation_time'] = int(rt)

    def change_reference_mic(self, ref_mic):
        self.sim_configs['reference_microphone'] = int(ref_mic)

    def change_snr(self, snr):
        self.sim_configs['SNR'] = int(snr)

    def change_absorbtion(self, state):
        self.sim_configs['air_absorbtion'] = state == Qt.Checked

    def change_ray_tracing(self, state):
        self.sim_configs['ray_tracing'] = state == Qt.Checked

    def load_parameters_to_data_and_destroy(self):
        self.load_parameters_to_data()
        self.hide()

    def load_parameters_to_data(self):
        with open('Data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
            d['Simulation parameters'] = self.sim_configs
        with open('Data.yaml', 'w') as f:
            yaml.dump(d, f, sort_keys=False, indent=4)


class Wall2D(__pybind11_builtins.pybind11_object):
    # no doc

    def area(self): # real signature unknown; restored from __doc__
        """ area(self: pyroomacoustics.libroom.Wall2D) -> float """
        return 0.0

    def __init__(self, corners, *args, **kwargs): # real signature unknown; NOTE: unreliably restored from __doc__
        """ __init__(self: pyroomacoustics.libroom.Wall2D, corners: numpy.ndarray[numpy.float32[2, n]],
        absorption: numpy.ndarray[numpy.float32[m, 1]] = array([0.],
        dtype=float32), scattering: numpy.ndarray[numpy.float32[m, 1]] = array([0.],
        dtype=float32), name: str = '') -> None """
        pass

    def intersection(self, arg0, *args, **kwargs):  # real signature unknown; NOTE: unreliably restored from __doc__
        """ intersection(self: pyroomacoustics.libroom.Wall2D, arg0: numpy.ndarray[numpy.float32[2, 1]],
        arg1: numpy.ndarray[numpy.float32[2, 1]], arg2: numpy.ndarray[numpy.float32[2, 1], flags.writeable]) -> int """
        pass

    def intersects(self, arg0, *args, **kwargs):  # real signature unknown; NOTE: unreliably restored from __doc__
        """ intersects(self: pyroomacoustics.libroom.Wall2D, arg0: numpy.ndarray[numpy.float32[2, 1]],
        arg1: numpy.ndarray[numpy.float32[2, 1]]) -> int """
        pass

    BNDRY = None  # (!) real value is '<Isect.BNDRY: 2>'
    dim = 2
    ENDPT = None  # (!) real value is '<Isect.ENDPT: 1>'
    Isect = None  # (!) real value is "<class 'pyroomacoustics.libroom.Wall.Isect'>"
    NONE = None  # (!) real value is '<Isect.NONE: -1>'
    VALID = None  # (!) real value is '<Isect.VALID: 0>'


    corners = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default


class Room_gui(object):
    def __init__(self, walls, sources=None, mics=None):
        self.walls = walls
        self.dim = walls[0].dim

        self.sources = []
        if sources is not None:
            for src in sources:
                self.add_source(src)

        self.mics = []
        if mics is not None:
            for mic in mics:
                self.add_microphone(mic)

    @classmethod
    def from_corners(cls, corners):
        """
        Creates a 2D room by giving an array of corners.

        Parameters
        ----------
        corners: (np.array dim 2xN, N>2)
            list of corners, must be antiClockwise oriented
        Returns
        -------
        Instance of a 2D room
        """
        # make sure the corners are wrapped in an ndarray
        corners = np.array(corners)
        n_walls = corners.shape[1]

        corners = np.array(corners)
        if corners.shape[0] != 2 or n_walls < 3:
            raise ValueError("Arg corners must be more than two 2D points.")

        walls = []
        for i in range(n_walls):
            walls.append(Wall2D(np.array([corners[:, i], corners[:, (i + 1) % n_walls]]).T))

        return cls(
            walls,
            sources=sources,
            mics=mics,
        )

        # We want to make sure the corners are ordered counter-clockwise
        #if libroom.area_2d_polygon(corners) <= 0:
        #   corners = corners[:, ::-1]

    def extrude(self, height, v_vec=None):
        """
    Creates a 3D room by extruding a 2D polygon.
    The polygon is typically the floor of the room and will have z-coordinate zero. The ceiling

    Parameters
    ----------
    height : float
        The extrusion height
    v_vec : array-like 1D length 3, optional
        A unit vector. An orientation for the extrusion direction. The
        ceiling will be placed as a translation of the floor with respect
        to this vector (The default is [0,0,1]).
    """

        if self.dim != 2:
            raise ValueError("Can only extrude a 2D room.")

        # default orientation vector is pointing up
        if v_vec is None:
            v_vec = np.array([0.0, 0.0, 1.0])

        # check that the walls are ordered counterclock wise
        # that should be the case if created from from_corners function

        nw = len(self.walls)
        floor_corners = np.zeros((2, nw))
        floor_corners[:, 0] = walls[0].corners[:, 0]
        """""
    ordered = True
    for iw, wall in enumerate(self.walls[1:]):
        if not np.allclose(self.walls[iw].corners[:, 1], wall.corners[:, 0]):
            ordered = False
        floor_corners[:, iw + 1] = wall.corners[:, 0]
    if not np.allclose(self.walls[-1].corners[:, 1], self.walls[0].corners[:, 0]):
        ordered = False

    if not ordered:
        raise ValueError(
            "The wall list should be ordered counter-clockwise, which is the case \
            if the room is created with Room.from_corners"
        )
    """""

        # make sure the floor_corners are ordered anti-clockwise (for now)
        #if libroom.area_2d_polygon(floor_corners) <= 0:
        #   floor_corners = np.fliplr(floor_corners)

        walls = []
        for i in range(nw):
            corners = np.array(
                [
                    np.r_[floor_corners[:, i], 0],
                    np.r_[floor_corners[:, (i + 1) % nw], 0],
                    np.r_[floor_corners[:, (i + 1) % nw], 0] + height * v_vec,
                    np.r_[floor_corners[:, i], 0] + height * v_vec,
                ]
            ).T
            walls.append(Wall2D(corners)
            )

    def plot(self, figsize=None, no_axis=False, mic_marker_size=10, plot_directivity=True, ax=None):
        """Plots the room with its walls, microphones and sources"""

        try:
            import matplotlib
            import matplotlib.pyplot as plt
            from matplotlib.collections import PatchCollection
            from matplotlib.patches import Circle, Polygon, Wedge
        except ImportError:
            import warnings

            warnings.warn("Matplotlib is required for plotting")
            return

        fig = None

        if self.dim == 3:
            import matplotlib.colors as colors
            import matplotlib.pyplot as plt
            import mpl_toolkits.mplot3d as a3
            import scipy as sp

            if ax is None:
                fig = plt.figure(figsize=figsize)
                ax = a3.Axes3D(fig)

            # plot the walls
            for w in self.walls:
                tri = a3.art3d.Poly3DCollection([w.corners.T], alpha=0.5)
                tri.set_color(colors.rgb2hex(sp.rand(3)))
                tri.set_edgecolor("k")
                ax.add_collection3d(tri)

            # define some markers for different sources and colormap for damping
            markers = ["o", "s", "v", "."]
            cmap = plt.get_cmap("YlGnBu")

            # use this to check some image sources were drawn
            #has_drawn_img = False

            # draw the scatter of images
            for i, source in enumerate(self.sources):
                # draw source
                ax.scatter(
                    source.x,        # source is an instance of soundsource class
                    source.y,
                    source.z,
                    c=[cmap(1.0)],
                    s=20,
                    marker=markers[i % len(markers)],
                    edgecolor=cmap(1.0),
                )

                """""
                if plot_directivity and source.directivity is not None:
                    azimuth_plot = np.linspace(
                        start=0, stop=360, num=361, endpoint=True
                    )
                    colatitude_plot = np.linspace(
                        start=0, stop=180, num=180, endpoint=True
                    )
                    
                    ax = source.directivity.plot_response(
                        azimuth=azimuth_plot,
                        colatitude=colatitude_plot,
                        degrees=True,
                        ax=ax,
                        offset=source.position,
                    )
                """""
                """"
                # draw images
                if img_order is None:
                    img_order = self.max_order

                I = source.orders <= img_order
                if len(I) > 0:
                    has_drawn_img = True
      
                val = (np.log2(np.mean(source.damping, axis=0)[I]) + 10.0) / 10.0
                # plot the images
                ax.scatter(
                    source.images[0, I],
                    source.images[1, I],
                    source.images[2, I],
                    c=cmap(val),
                    s=20, #Creates a 3D room by extruding a 2D polygon
                    marker=markers[i % len(markers)],
                    edgecolor=cmap(val),
                )

            # When no image source has been drawn, we need to use the bounding box
            # to set correctly the limits of the plot
            if not has_drawn_img or img_order == 0:
                bbox = self.get_bbox()
                ax.set_xlim3d(bbox[0, :])
                ax.set_ylim3d(bbox[1, :])
                ax.set_zlim3d(bbox[2, :])
            """""

            # draw the microphones
            if self.mics is not None:                 #mic is an instance of microphone class
                for i in range(len(self.mics)):
                    #ax.scatter(self.mic_array.R[0][i], self.mic_array.R[1][i], self.mic_array.R[2][i], marker="x",
                    #   linewidth=0.5, s=mic_marker_size, c="k" )

                    ax.scatter(self.mics[i].x, self.mics[i].y, self.mics[i].z, marker="x",
                       linewidth=0.5, s=mic_marker_size, c="k" )

                    """""
                    if plot_directivity and self.mic_array.directivity is not None:
                        azimuth_plot = np.linspace(
                            start=0, stop=360, num=361, endpoint=True
                        )
                    
                    colatitude_plot = np.linspace(start=0, stop=180, num=180, endpoint=True)
                    ax = self.mic_array.directivity[i].plot_response(
                        azimuth=azimuth_plot,
                        colatitude=colatitude_plot,
                        degrees=True,
                        ax=ax,
                        offset=self.mic_array.R[:, i])
                    """""

        return fig, a

    def is_inside(self, p, include_borders=True):
        """
        Checks if the given point is inside the room.

        Parameters
        ----------
        p: array_like, length 2 or 3
            point to be tested
        include_borders: bool, optional
            set true if a point on the wall must be considered inside the room

        Returns
        -------
            True if the given point is inside the room, False otherwise.
        """
        p = np.array(p)
        if self.dim != p.shape[0]:
            raise ValueError("Dimension of room and p must match.")

        # The method works as follows: we pick a reference point *outside* the room and
        # draw a line between the point to check and the reference.
        # If the point to check is inside the room, the line will intersect an odd
        # number of walls. If it is outside, an even number.
        # Unfortunately, there are a lot of corner cases when the line intersects
        # precisely on a corner of the room for example, or is aligned with a wall.

        # To avoid all these corner cases, we will do a randomized test.
        # We will pick a point at random outside the room so that the probability
        # a corner case happen is virtually zero. If the test raises a corner
        # case, we will repeat the test with a different reference point.

        # get the bounding box
        bbox = self.get_bbox()
        bbox_center = np.mean(bbox, axis=1)
        bbox_max_dist = np.linalg.norm(bbox[:, 1] - bbox[:, 0]) / 2

        # re-run until we get a non-ambiguous result
        it = 0
        while it < constants.get("room_isinside_max_iter"):

            # Get random point outside the bounding box
            random_vec = np.random.randn(self.dim)
            random_vec /= np.linalg.norm(random_vec)
            p0 = bbox_center + 2 * bbox_max_dist * random_vec

            ambiguous = False  # be optimistic
            is_on_border = False  # we have to know if the point is on the boundary
            count = 0  # wall intersection counter
            for i in range(len(self.walls)):
                # intersects, border_of_wall, border_of_segment = self.walls[i].intersects(p0, p)
                # ret = self.walls[i].intersects(p0, p)
                loc = np.zeros(self.dim, dtype=np.float32)
                ret = self.walls[i].intersection(p0, p, loc)

                if (
                        ret == int(Wall2D.Isect.ENDPT) or ret == 3
                ):  # this flag is True when p is on the wall
                    is_on_border = True

                elif ret == Wall2D.Isect.BNDRY:
                    # the intersection is on a corner of the room
                    # but the point to check itself is *not* on the wall
                    # then things get tricky
                    ambiguous = True

                # count the wall intersections
                if ret >= 0:  # valid intersection
                    count += 1

            # start over when ambiguous
            if ambiguous:
                it += 1
                continue

            else:
                if is_on_border and not include_borders:
                    return False
                elif is_on_border and include_borders:
                    return True
                elif count % 2 == 1:
                    return True
                else:
                    return False

        return False

        # We should never reach this
        #raise ValueError(
            #Error could not determine if point is in or out in maximum number of iterations.
            #This is most likely a bug, please report it.
        #)

    def add(self, obj):
        """
        Adds a sound source or microphone to a room

        Parameters
        ----------
        obj: :py:obj:`~Sim_room_classes.soundsource` or :py:obj:`~Sim_room_classes.microphone` object
                    The object to add

        Returns
        -------
        :py:obj:`~Room_gui object
            The room is returned for further tweaking.
        """

        if isinstance(obj, soundsource):
            if not self.is_inside(np.array[obj.x, obj.y, obj.z]):
                raise ValueError("The source must be added inside the room.")

            self.sources.append(obj)

        elif isinstance(obj, microphone):
            if not self.is_inside(np.array[obj.x, obj.y, obj.z]):
                raise ValueError("The microphone must be added inside the room.")

            self.mics.append(obj)

        return self

    def add_source(self, loc):
        """
        Adds a sound source given by its position in the room.
        Parameters
        -----------
        loc: ndarray, shape: (3,)
            The location of the source in the room_configs
        Returns
        -------
        :py:obj:`room
            The room is returned for further tweaking.
        """
        loc = np.array(loc)

        return self.add(soundsource(x=loc[0], y=loc[1], z=loc[2], muted=0))

    def add_microphone(self, loc):
        """
        Adds a single microphone in the room.

        Parameters
        ----------
        loc: array_like or ndarray
            The location of the microphone. The length should be the same as the room dimension.

        Returns
        -------
        obj - room
             The room is returned for further tweaking.
        """
        loc = np.array(loc)

        return self.add(microphone(x=loc[0], y=loc[1], z=loc[2], muted=0))


if __name__ == "__main__":
    # import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())