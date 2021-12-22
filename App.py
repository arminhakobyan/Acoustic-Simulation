import sys
import yaml
from yaml.loader import SafeLoader
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui, QtWidgets, QtCore
from Sim_room_classes import *
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
    QMenuBar,
    QStatusBar,
    QFrame,
    QPushButton,
    QComboBox,
    QCheckBox,
    QRadioButton,
    QGroupBox,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('My app')
        geometry = app.desktop().availableGeometry()
        self.setGeometry(geometry)

        self.source_window = SourceWindow()
        self.microphone_window = MicrophoneWindow()
        self.room_window = RoomWindow()
        self.sim_parameters_window = SimulationParametersWindow()

        layout = QHBoxLayout()
        layout_mic_sources_player = QVBoxLayout()
        layout_room_sins = QVBoxLayout()

        layout_mic_sources_player.addWidget(QLabel('Sources info'))
        layout_mic_sources_player.addWidget(QLabel('Microphones info'))
        layout_mic_sources_player.addWidget(QLabel('Player'))

        layout.addLayout(layout_mic_sources_player)

        layout_room_sins.addWidget(QLabel('Room graphic'))
        layout_room_sins.addWidget(QLabel('Source sinusoide'))
        layout_room_sins.addWidget(QLabel('Mic sinusoide'))
        layout.addLayout(layout_room_sins)

        widget = QWidget()
        widget.setLayout(layout)
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
        run_action.triggered.connect(self.onMenuBarFileClick)
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

        simulate_menu = menu.addMenu("Configs")
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


class SourceWindow(QWidget):
    def __init__(self):
        super(SourceWindow, self).__init__()
        self.setWindowTitle("Sources")
        self.setGeometry(150, 80, 450, 420)

        with open('Initial_configs.yaml') as f:
            data = yaml.load(f, Loader=FullLoader)
        self.source_configs = data['Sources']

        with open('buffer_data.yaml') as f:
            self.buffer = yaml.load(f, Loader=FullLoader)['Sources']

        # self.layout = QVBoxLayout()
        self.layout = QGridLayout()
        self.layout1 = QGridLayout()  # select source,  mute/remove, functional/wav file
        self.layout_form = QGridLayout()
        # self.layout_func = QGridLayout()  #parameters functional or wav file
        # self.layout_file = QGridLayout()

        self.layout5 = QHBoxLayout()  # apply/cancel/ok buttons

        # layout1
        self.sources = QComboBox()
        self.sources.setEditable(True)  # to add sources

        self.mute_box = QCheckBox("Mute")
        self.mute_box.setCheckable(True)
        self.rmmove_box = QCheckBox("Remove")
        self.rmmove_box.setCheckable(True)

        self.x_pos_line_edit = QLineEdit()
        self.x_pos_line_edit.setPlaceholderText("X coordinate")
        self.y_pos_line_edit = QLineEdit()
        self.y_pos_line_edit.setPlaceholderText("Y coordinate")
        self.z_pos_line_edit = QLineEdit()
        self.z_pos_line_edit.setPlaceholderText("Z coordinate")
        self.func_radiobtn = QRadioButton("Functional")
        self.file_radiobtn = QRadioButton("Wav file")

        self.layout1.addWidget(self.sources, 0, 0)
        self.layout1.addWidget(self.mute_box, 0, 2)
        self.layout1.addWidget(self.rmmove_box, 0, 3)
        self.layout1.addWidget(self.func_radiobtn, 1, 0)
        self.layout1.addWidget(self.file_radiobtn, 1, 1)
        self.layout1.addWidget(QLabel("Position"), 2, 0)
        self.layout1.addWidget(self.x_pos_line_edit, 2, 1)
        self.layout1.addWidget(self.y_pos_line_edit, 2, 2)
        self.layout1.addWidget(self.z_pos_line_edit, 2, 3)

        # func form widgets
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

        self.func_widgets = [self.amp_label, self.amp_line_edit, self.freq_label, self.freq_line_edit, self.fs_label_,
                             self.fs_line_edit_, self.phase_label, self.phase_line_edit, self.time_label,
                             self.time_line_edit]

        # file form widgets
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

        self.initialize_entries('Source1')

        self.sources.currentIndexChanged.connect(self.source_index_changed)
        self.sources.currentTextChanged.connect(self.sources_text_changed)
        # QComboBox.InsertBeforeCurrent- insert will be handled like this -
        # Insert before current item(before add source item)
        self.sources.setInsertPolicy(QComboBox.InsertBeforeCurrent)

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

        self.btn_ok.clicked.connect(self.load_parameters_to_data_and_destroy)
        self.btn_apply.clicked.connect(self.load_parameters_to_buffer)
        self.btn_cancel.clicked.connect(self.hide)

        self.layout.addLayout(self.layout1, 0, 0)
        self.layout.addLayout(self.layout_form, 1, 0)
        self.layout.addLayout(self.layout5, 2, 0)
        self.setLayout(self.layout)

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

    def sources_text_changed(self, text):
        print(text)

    def to_functional(self, selected):
        if selected:
            for i in range(len(self.file_widgets)):
                self.file_widgets[i].hide()
            for i in range(len(self.func_widgets)):
                self.func_widgets[i].show()

    def to_wav_file(self, selected):
        if selected:
            for i in range(len(self.func_widgets)):
                self.func_widgets[i].hide()
            for i in range(len(self.file_widgets)):
                self.file_widgets[i].show()

    def browse_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Single File', QtCore.QDir.rootPath(), '*.wav')
        self.file_lineedit.setText(filename)

    def change_mute_state(self, state):
        if state == True:
            print(state)  # tesnel vor sourcena comboboxum, u ira bufferi muted=1 dnel

    def change_remove_state(self, state):
        if state == True:
            print(state)  # tesnel vor sourcena comboboxum, u iran remove anel

    def initialize_entries(self, s: str):
        for i in range(len(self.source_configs)):
            self.sources.addItem('Source' + str(i + 1))
        self.sources.addItem("Add Source")

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

        # if self.source_configs[s]['muted'] == 0:
        func_s = self.source_configs[s]['functional_form']
        file_s = self.source_configs[s]['wav file']

        self.x_pos_line_edit.setText(str(func_s['x']))
        self.y_pos_line_edit.setText(str(func_s['y']))
        self.z_pos_line_edit.setText(str(func_s['z']))

        if self.source_configs[s]['form'] == 0:  # functional form
            self.func_radiobtn.setChecked(True)
            self.to_functional(True)
            self.file_radiobtn.setChecked(False)
        else:  # file form
            self.file_radiobtn.setChecked(True)
            self.to_wav_file(True)
            self.func_radiobtn.setChecked(False)

        self.amp_line_edit.setText(str(func_s['amplitude']))
        self.fs_line_edit_.setText(str(func_s['fs']))
        self.freq_line_edit.setText(str(func_s['frequency']))
        self.phase_line_edit.setText(str(func_s['phase']))
        self.time_line_edit.setText(str(func_s['time']))

        self.file_lineedit.setText(file_s['filename'])
        self.tstart_lineedit.setText(str(file_s['t_start']))
        self.tend_lineedit.setText(str(file_s['t_end']))
        self.t_lineedit.setText(str(file_s['time']))
        self.fs_lineedit.setText(str(file_s['fs']))

    def load_parameters_to_data_and_destroy(self):
        with open('Data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
        d['Sources'] = self.buffer

        with open('Data.yaml', 'w') as f:
            yaml.dump(d, f)
        self.hide()

    def load_parameters_to_buffer(self):
        with open('buffer_data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
        d['Sources'] = self.buffer
        with open('buffer_data.yaml', 'w') as f:
            yaml.dump(d, f)


class MicrophoneWindow(QWidget):
    def __init__(self):
        super(MicrophoneWindow, self).__init__()
        self.setWindowTitle("Microphones")
        self.setGeometry(150, 80, 550, 250)

        layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout3 = QHBoxLayout()

        self.microphones = QComboBox()
        self.microphones.setEditable(True)  # to add sources
        self.microphones.addItems(["Microphone 1", "Add Microphone"])
        self.microphones.currentIndexChanged.connect(self.microphone_index_changed)
        self.microphones.currentTextChanged.connect(self.microphone_text_changed)
        # QComboBox.InsertBeforeCurrent- insert will be handled like this - Insert before current item(before add source item)
        self.microphones.setInsertPolicy(QComboBox.InsertBeforeCurrent)

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
        self.filepath_line_edit.setPlaceholderText("file path")

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

        layout3.addWidget(self.btn_apply)
        layout3.addWidget(self.btn_cancel)
        layout3.addWidget(self.btn_ok)

        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addLayout(layout3)
        self.setLayout(layout)

    def microphone_index_changed(self, index):
        print("Microphone", index)

    def microphone_text_changed(self, text):
        print(text)

    def show_state(self, state):
        print(state == Qt.Checked)
        print(state)


class RoomWindow(QWidget):
    def __init__(self):
        super(RoomWindow, self).__init__()
        self.setWindowTitle("Room")
        self.setGeometry(150, 80, 350, 400)

        with open('Initial_configs.yaml') as f:
            self.data = yaml.load(f, Loader=FullLoader)
        self.room_configs = self.data['Room']

        layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout2 = QHBoxLayout()

        self.length_lineedit = QLineEdit()
        self.width_lineedit = QLineEdit()
        self.height_lineedit = QLineEdit()
        self.temp_lineedit = QLineEdit()
        self.humadity_lineedit = QLineEdit()

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
        self.btn_ok.clicked.connect(self.load_parameters_to_data_and_destroy)
        self.btn_apply.clicked.connect(self.load_parameters_to_data)
        self.btn_cancel.clicked.connect(self.hide)

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

    def wall_material_changed(self, material_ind):
        self.walls.setCurrentIndex(self.data['Material values'].index(material_ind))
        self.room_configs['walls'] = self.data['Material values'].index(material_ind)

    def floor_material_changed(self, material_ind):
        self.floor.setCurrentIndex(self.data['Material values'].index(material_ind))
        self.room_configs['Room']['floor'] = self.data['Material values'].index(material_ind)

    def load_parameters_to_data_and_destroy(self):
        self.load_parameters_to_data()
        self.hide()

    def load_parameters_to_data(self):
        with open('Data.yaml') as f:
            d = yaml.load(f, Loader=FullLoader)
            d['Room'] = self.room_configs
        with open('Data.yaml', 'w') as f:
            yaml.dump(d, f, sort_keys=False, indent=4)


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
