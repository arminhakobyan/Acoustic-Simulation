import sys
import time
import yaml
from Sim_room_classes import *
import numpy as np
from PyQt5.QtCore import Qt, QRect
from PyQt5 import QtGui, QtWidgets, QtCore
from Sim_room_classes import *
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qt5agg import (FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
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
    QScrollArea,
    QGroupBox,
)

class ClickableLabel(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)

    clicked = QtCore.pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        QLabel.mousePressEvent(self, event)

    """"
    def mousePressEvent(self, event):
        self.emit(SIGNAL("clicked()"))
        QLabel.mousePressEvent(self, event)
    """""

class ScrollArea(QScrollArea):
    def __init__(self, parent=None, objectName="", objectCount=0):
        super(ScrollArea, self).__init__(parent)
        self.objectName = objectName
        self.objectCount = objectCount
        self.setFixedSize(630, 200)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)

        container = QWidget()
        self.setWidget(container)
        vbox = QVBoxLayout(container)
        self.obj_labels = []

        for i in range(objectCount+1):
            hbox = QHBoxLayout()
            groupbox = QGroupBox()
            groupbox.setFixedSize(600, 100)

            if i == self.objectCount:
                self.add_lb = ClickableLabel('Add '+self.objectName)
                self.obj_labels.append(self.add_lb)
                hbox.addWidget(self.add_lb)
            else:
                self.lb = ClickableLabel(self.objectName + "%s" % (i + 1))
                self.obj_labels.append(self.lb)
                self.play = QPushButton("Play")
                self.pause = QPushButton("Pause")
                self.stop = QPushButton("Stop")
                self.mutecheckbox = QCheckBox('Mute')
                self.removecheckbox = QCheckBox('Remove')

                hbox.addWidget(self.lb)
                hbox.addWidget(self.play)
                hbox.addWidget(self.pause)
                hbox.addWidget(self.stop)
                hbox.addWidget(self.mutecheckbox)
                hbox.addWidget(self.removecheckbox)

            groupbox.setLayout(hbox)

            vbox.addLayout(hbox)
            vbox.addWidget(groupbox)

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
        if configs['Sources'][source]['functional_form']['muted'] == 1 or configs['Sources'][source]['wav file']['muted'] == 1:
            continue
        else:
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

class _Widget(QtWidgets.QWidget):
    def __init__(self):
        super(_Widget, self).__init__()
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.room = create_sim_room()
        self.fig_room, self.ax = self.room.room.plot(mic_marker_size=30, figsize=(5, 3))
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
        self.sourceScrollArea = ScrollArea(parent=None, objectName="Source", objectCount=2)
        self.layout_left.addWidget(self.sourceScrollArea)
        for i in range(len(self.sourceScrollArea.obj_labels)):
            #self.sourceScrollArea.obj_labels[i].mousePressEvent = self.show_source_from_Sources_window
            self.sourceScrollArea.obj_labels[i].clicked.connect(self.show_source_from_Sources_window)

        self.micScrollArea = ScrollArea(parent=None, objectName="Microphone", objectCount=1)
        self.layout_left.addWidget(self.micScrollArea)
        for i in range(len(self.micScrollArea.obj_labels)):
            #self.micScrollArea.obj_labels[i].mousePressEvent = self.show_mic_from_Microphones_window
            self.micScrollArea.obj_labels[i].clicked.connect(self.show_mic_from_Microphones_window)

        self.layout_left.addWidget(QLabel('Player'))

        # right side vertical layout, where should be plots for room, sound and mic waveforms
        self.layout_right = QVBoxLayout()

        # room canvas
        self.canvas = CanvasWidget()
        self.layout_right.setContentsMargins(0, 0, 0, 0)
        self.layout_right.addWidget(self.canvas)
        self.layout_right.addWidget(QLabel('sinusoides'))

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

    def show_source_from_Sources_window(self):
        self.show_Sources_window()
        sender = self.sender()
        self.source_window.sources.setCurrentText(sender.text())
        self.source_window.source_changed(s=sender.text())

    def show_Microphones_window(self):
        if self.microphone_window.isVisible():
            self.microphone_window.hide()
        else:
            self.microphone_window.show()

    def show_mic_from_Microphones_window(self):
        self.show_Microphones_window()
        sender = self.sender()
        self.microphone_window.microphones.setCurrentText(sender.text())
        self.microphone_window.mic_changed(m=sender.text())

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
        self.sources_box = QComboBox()
        self.sources_box.setEditable(True)  # to add sources
        self.sources = []
        for i in range(len(self.buffer)):
            self.sources.append('Source' + str(i + 1))
        self.sources.append("Add Source")

        self.sources_box.addItems(self.sources)
        print(self.sources)

        self.mute_box = QCheckBox("Mute")
        self.mute_box.setCheckable(True)
        self.remove_label = ClickableLabel('Remove')

        self.removed_sources = []

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
        self.layout1.addWidget(self.sources_box, 0, 0)
        self.layout1.addWidget(self.mute_box, 0, 2)
        self.layout1.addWidget(self.remove_label, 0, 3)
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

        # after creating all widgets, initialize them with buffer values
        self.initialize_source_window()
        if len(self.buffer) != 0:
            self.filling_entries('Source1')

        # source change operation connect to source_changed method
        self.sources_box.currentTextChanged.connect(self.source_changed)
        # QComboBox.InsertBeforeCurrent- insert will be handled like this -
        # Insert before current item(before add source item) - for adding source
        self.sources_box.setInsertPolicy(QComboBox.InsertAfterCurrent)

        # function/wav file selection connect to-
        # to_functional method for functional form and
        # to_wav_file method for wav file form
        # same for mute/ remove checkboxes, and browse button and etc
        self.func_radiobtn.toggled.connect(self.to_functional)
        self.file_radiobtn.toggled.connect(self.to_wav_file)
        self.mute_box.stateChanged.connect(self.change_mute_state)
        #self.remove_box.stateChanged.connect(self.change_remove_state)
        self.remove_label.clicked.connect(self.remove_source_action)
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
        source = str(self.sources_box.currentText())
        if amplitude == "":
            amplitude = 0
        self.buffer[source]['functional_form']['amplitude'] = int(amplitude)

    def get_frequency(self, freq: str):
        source = str(self.sources_box.currentText())
        if freq == "":
            freq = 0
        self.buffer[source]['functional_form']['frequency'] = int(freq)

    def get_fs_func(self, fs: str):
        source = str(self.sources_box.currentText())
        if fs == "":
            fs = 0
        self.buffer[source]['functional_form']['fs'] = int(fs)

    def get_phase(self, phase: str):
        source = str(self.sources_box.currentText())
        if phase == "":
            phase = 0
        self.buffer[source]['functional_form']['phase'] = int(phase)

    def get_time_func(self, time: str):
        source = str(self.sources_box.currentText())
        if time == "":
            time = 0
        self.buffer[source]['functional_form']['time'] = int(time)

    # ---- file form ---
    def get_file(self, file: str):
        source = str(self.sources_box.currentText())
        if file == "":
            file = " "
        self.buffer[source]['wav file']['filename'] = file

    def get_start_time(self, stime: str):
        source = str(self.sources_box.currentText())
        if stime == "":
            stime = 0
        self.buffer[source]['wav file']['t_start'] = int(stime)

    def get_end_time(self, etime: str):
        source = str(self.sources_box.currentText())
        if etime == "":
            etime = 0
        self.buffer[source]['wav file']['t_end'] = int(etime)

    def get_time_fileform(self, time: str):
        source = str(self.sources_box.currentText())
        if time == "":
            time = 0
        self.buffer[source]['wav file']['time'] = float(time)

    def get_fs_fileform(self, fs: str):
        source = str(self.sources_box.currentText())
        if fs == "":
            fs = 0
        self.buffer[source]['wav file']['fs'] = int(fs)

    def get_x(self, x: str):
        source = str(self.sources_box.currentText())
        if x == "":
            x = 0
        self.buffer[source]['wav file']['x'] = int(x)
        self.buffer[source]['functional_form']['x'] = int(x)

    def get_y(self, y: str):
        source = str(self.sources_box.currentText())
        if y == "":
            y = 0
        self.buffer[source]['wav file']['y'] = int(y)
        self.buffer[source]['functional_form']['y'] = int(y)

    def get_z(self, z: str):
        source = str(self.sources_box.currentText())
        if z == "":
            z = 0
        self.buffer[source]['wav file']['z'] = int(z)
        self.buffer[source]['functional_form']['z'] = int(z)

    def source_index_changed(self, index):
        print("Source", index)

    def add_new_source(self, new_source_ind: int, new_source: str):
        self.buffer[new_source] = {}
        self.buffer[new_source]['form'] = 0

        self.buffer[new_source]['functional_form'] = {}
        self.buffer[new_source]['wav file'] = {}
        self.buffer[new_source]['functional_form']['amplitude'] = 0
        self.buffer[new_source]['functional_form']['frequency'] = 0
        self.buffer[new_source]['functional_form']['fs'] = 0
        self.buffer[new_source]['functional_form']['phase'] = 0
        self.buffer[new_source]['functional_form']['time'] = 0
        self.buffer[new_source]['functional_form']['x'] = 0
        self.buffer[new_source]['functional_form']['y'] = 0
        self.buffer[new_source]['functional_form']['z'] = 0
        self.buffer[new_source]['functional_form']['muted'] = 0

        self.buffer[new_source]['wav file']['filename'] = ""
        self.buffer[new_source]['wav file']['fs'] = 0
        self.buffer[new_source]['wav file']['t_start'] = 0
        self.buffer[new_source]['wav file']['t_end'] = 0
        self.buffer[new_source]['wav file']['time'] = 0
        self.buffer[new_source]['wav file']['x'] = 0
        self.buffer[new_source]['wav file']['y'] = 0
        self.buffer[new_source]['wav file']['z'] = 0
        self.buffer[new_source]['wav file']['muted'] = 0

        self.sources_box.insertItem(new_source_ind, new_source)
        self.sources.append(new_source)

    def source_changed(self, s: str):
        if s != 'Add Source':
            self.filling_entries(s)
        else:
            new_source_ind = self.sources_box.currentIndex()
            new_source = 'Source' + str(new_source_ind+1)
            self.add_new_source(new_source_ind, new_source)
            self.sources_box.setCurrentText(new_source)
            self.source_changed(new_source)

    def to_functional(self, selected):
        if selected:
            for i in range(len(self.file_widgets)):
                self.file_widgets[i].hide()
            for i in range(len(self.func_widgets)):
                self.func_widgets[i].show()

            source = str(self.sources_box.currentText())
            self.buffer[source]['form'] = 0  # source is functional form(0-func form)

    def to_wav_file(self, selected):
        if selected:
            for i in range(len(self.func_widgets)):
                self.func_widgets[i].hide()
            for i in range(len(self.file_widgets)):
                self.file_widgets[i].show()
            source = str(self.sources_box.currentText())
            self.buffer[source]['form'] = 1  # source is wav form(1-file form)

    def browse_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*.wav')
        self.file_lineedit.setText(filename)

    def change_mute_state(self):
        s = self.sources_box.currentText()
        if self.mute_box.isChecked():
            self.buffer[s]['functional_form']['muted'] = 1
            self.buffer[s]['wav file']['muted'] = 1
        else:
            self.buffer[s]['functional_form']['muted'] = 0
            self.buffer[s]['wav file']['muted'] = 0

    """"
    def change_remove_state(self):
        s = self.sources.currentText()
        if self.remove_box.isChecked():
            del self.buffer[s]

        print(self.buffer)
    """""

    """""
    def update_sources(self, removed_ind: int, count_sources: int):
        if count_sources > 1 and removed_ind != count_sources - 1:
            for j in range(count_sources - removed_ind - 1):
                self.sources.setItemText(removed_ind + j, 'Source' + str(removed_ind + j + 1))

        if count_sources > 0 and removed_ind != count_sources:
            for j in range(count_sources - removed_ind):
                self.buffer['Source' + str(removed_ind+j+1)] = self.buffer['Source' + str(removed_ind+j+2)]
                del self.buffer['Source' + str(removed_ind+j+2)]
    """""

    def remove_source_action(self):
        s = self.sources.currentText()
        ind = self.sources.currentIndex()
        if self.remove_label.text() == 'Remove':
            self.remove_label.setText('Removed')
            self.removed_sources.append(ind)
        else:
            self.remove_label.setText('Remove')
            self.removed_sources.remove(ind)
        #del self.buffer[s]
        #self.sources.removeItem(ind)


        #self.update_sources(removed_ind=ind, count_sources=count)
        """""
        sources_count = self.sources.count()
        if sources_count > 1 and ind != sources_count-1:
            for j in range(sources_count-ind-1):
                self.sources.setItemText(ind+j, 'Source'+str(ind+j+1))
        """""

    """""
    def update_sources(self):
        if len(self.removed_sources) != 0:
            for j in range(len(self.removed_sources)):
                removed_ind = self.removed_sources[j]
                self.sources.removeItem(removed_ind)
                del self.buffer['Source' + str(removed_ind+1)]

            sources_count = self.sources.count()-1
            for i in range(sources_count):
                self.sources.setItemText(index=i, text='Source' + str(i+1))

            for j in range(len(self.removed_sources)):
                removed_ind = self.removed_sources[j]
                if count_sources > 0 and removed_ind != count_sources:
                    for k in range(count_sources - removed_ind):
                        self.buffer['Source' + str(removed_ind + k + 1)] = self.buffer['Source' + str(removed_ind + k + 2)]
                        del self.buffer['Source' + str(removed_ind + k + 2)]
            print(self.buffer)

        self.removed_sources = []
    """""

    def remove_sources_from_buffer(self):
        if len(self.removed_sources) != 0:
            for j in range(len(self.removed_sources)):
                removed_ind = self.removed_sources[j]
                del self.buffer['Source' + str(removed_ind + 1)]
                self.sources_box.removeItem(removed_ind)
                self.sources.remove(removed_ind)
            self.removed_sources.clear()
            self.remove_label.setText("Remove")

    def update_sources(self):
        #if len(self.removed_sources) != 0
        sources_count = len(self.sources) - 1
        for i in range(sources_count):
            self.sources.setItemText(index=i, text='Source' + str(i + 1))

            """""
            for j in range(len(self.removed_sources)):
                removed_ind = self.removed_sources[j]
                if count_sources > 0 and removed_ind != count_sources:
                    for k in range(count_sources - removed_ind):
                        self.buffer['Source' + str(removed_ind + k + 1)] = self.buffer[
                            'Source' + str(removed_ind + k + 2)]
                        del self.buffer['Source' + str(removed_ind + k + 2)]
            """""
        print(self.sources.items())
        #self.removed_sources = []

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
        self.func_s = self.buffer[s]['functional_form']
        self.file_s = self.buffer[s]['wav file']

        if self.func_s['muted'] == 1 or self.file_s['muted'] == 1:
            self.mute_box.setChecked(True)
        else:
            self.mute_box.setChecked(False)

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

        index = self.sources_box.currentIndex()
        print(index)
        if index in self.removed_sources:
            self.remove_label.setText('Removed')
        else:
            self.remove_label.setText('Remove')

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
        #self.update_sources()
        self.refresh_parameters()
        with open('Data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)

        d['Sources'] = self.buffer
        with open('Data.yaml', 'w') as f:
            yaml.dump(d, f)

        self.hide()

    # connected to apply button, for updating buffer data
    def refresh_parameters(self):
        self.remove_sources_from_buffer()
        #self.update_sources()
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


if __name__ == "__main__":
    # import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())




