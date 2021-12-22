import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
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

        room_pic = QLabel()
        souunsin_pic = QLabel()
        micsin_pic = QLabel()

        self.frame_sources = QGroupBox(self)
        self.frame_sources.setTitle("Sources")
        self.frame_sources.setMaximumWidth(600)
        self.frame_sources.setMaximumHeight(250)


        self.frame_mics = QGroupBox(self)
        self.frame_mics.setTitle("Microphones")
        self.frame_mics.setMaximumWidth(600)
        self.frame_mics.setMaximumHeight(250)

        self.frame_player = QGroupBox(self)
        self.frame_player.setTitle("Player")
        self.frame_player.setMaximumWidth(600)
        self.frame_player.setMaximumHeight(250)

        room_pic.setPixmap(QPixmap('room_graphics.jpg'))
        souunsin_pic.setPixmap(QPixmap('sound_sin.jpg'))
        micsin_pic.setPixmap(QPixmap('mic_sin.jpg'))

        layout = QHBoxLayout()
        layout_mic_sources_player = QVBoxLayout()
        layout_room_sins = QVBoxLayout()

        layout_mic_sources_player.addWidget(self.frame_sources)
        layout_mic_sources_player.addWidget(self.frame_mics)

        layout_mic_sources_player.addWidget(self.frame_player)
        layout.addLayout(layout_mic_sources_player)

        layout_room_sins.addWidget(room_pic)
        layout_room_sins.addWidget(souunsin_pic)
        layout_room_sins.addWidget(micsin_pic)
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
        self.setGeometry(150, 80, 500, 450)

        layout = QVBoxLayout()
        layout1 = QGridLayout()    # select source,  mute/remove, functional/wav file
        layout2 = QGridLayout()    # parameters
        layout4 = QHBoxLayout()    # apply/cancel/ok buttons


        # layout1
        self.sources = QComboBox()
        self.sources.setEditable(True)   # to add sources
        self.sources.addItems(["Source 1", "Source 2", "Add Source"])
        self.sources.currentIndexChanged.connect(self.source_index_changed)
        self.sources.currentTextChanged.connect(self.sources_text_changed)
        # QComboBox.InsertBeforeCurrent- insert will be handled like this - Insert before current item(before add source item)
        self.sources.setInsertPolicy(QComboBox.InsertBeforeCurrent)

        self.func_radiobtn = QRadioButton("Functional")
        self.func_radiobtn.setChecked(True)
        self.file_radiobtn = QRadioButton("Wav file")
        self.file_radiobtn.setChecked(False)

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

        layout1.addWidget(self.sources, 0, 0)
        layout1.addWidget(self.mute_box, 0, 2)
        layout1.addWidget(self.rmmove_box, 0, 3)
        layout1.addWidget(self.func_radiobtn, 1, 0)
        layout1.addWidget(self.file_radiobtn, 1, 1)
        layout1.addWidget(self.position_label, 2, 0)
        layout1.addWidget(self.x_pos_line_edit, 2, 1)
        layout1.addWidget(self.y_pos_line_edit, 2, 2)
        layout1.addWidget(self.z_pos_line_edit, 2, 3)
        layout.addLayout(layout1)

        self.amplitude_label = QLabel("Amplitde")
        self.amp_line_edit = QLineEdit()
        self.frequency_label = QLabel("Frequency")
        self.freq_line_edit = QLineEdit()
        self.fs_label = QLabel("Sampling freqyuency")
        self.fs_line_edit = QLineEdit()
        self.phase_label = QLabel("Phase")
        self.phase_line_edit = QLineEdit()
        self.time_label = QLabel("Time")
        self.time_line_edit = QLineEdit()

        layout2.addWidget(self.amplitude_label, 0, 0)
        layout2.addWidget(self.amp_line_edit, 0, 1)
        layout2.addWidget(self.frequency_label, 1, 0)
        layout2.addWidget(self.freq_line_edit, 1, 1)
        layout2.addWidget(self.fs_label, 2, 0)
        layout2.addWidget(self.fs_line_edit, 2, 1)
        layout2.addWidget(self.phase_label, 0, 2)
        layout2.addWidget(self.phase_line_edit, 0, 3)
        layout2.addWidget(self.time_label, 1, 2)
        layout2.addWidget(self.time_line_edit, 1, 3)

        layout.addLayout(layout2)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setStyleSheet("color: white;")
        self.btn_ok.setStyleSheet("Background-color: grey;")
        self.btn_apply = QPushButton("Apply")
        self.btn_apply.setStyleSheet("Background-color: grey;")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("Background-color: grey;")

        layout4.addWidget(self.btn_apply)
        layout4.addWidget(self.btn_cancel)
        layout4.addWidget(self.btn_ok)

        layout.addLayout(layout4)
        self.setLayout(layout)

    def source_index_changed(self, index):
        print("Source", index)

    def sources_text_changed(self, text):
        print(text)

    def show_state(self, state):
        print(state == Qt.Checked)
        print(state)


class MicrophoneWindow(QWidget):
    def __init__(self):
        super(MicrophoneWindow, self).__init__()
        self.setWindowTitle("Microphones")
        self.setGeometry(150, 80, 550, 250)

        layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout3 = QHBoxLayout()

        self.microphones = QComboBox()
        self.microphones.setEditable(True)   # to add sources
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
        self.setGeometry(150, 80, 350, 500)

        layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout2 = QHBoxLayout()

        self.sizes_label = QLabel("Sizes")

        self.length_lineedit = QLineEdit()
        self.length_lineedit.setPlaceholderText("Length")
        self.width_lineedit = QLineEdit()
        self.width_lineedit.setPlaceholderText("Width")
        self.height_lineedit = QLineEdit()
        self.height_lineedit.setPlaceholderText("Height")

        layout1.addWidget(self.sizes_label, 0, 0)
        layout1.addWidget(self.length_lineedit, 1, 1)
        layout1.addWidget(self.width_lineedit, 2, 1)
        layout1.addWidget(self.height_lineedit, 3, 1)

        self.environment_label = QLabel("Environment")
        self.temp_lineedit = QLineEdit()
        self.temp_lineedit.setPlaceholderText("Temperature")
        self.humadity_lineedit = QLineEdit()
        self.humadity_lineedit.setPlaceholderText("Humadity")

        layout1.addWidget(self.environment_label, 4, 0)
        layout1.addWidget(self.temp_lineedit, 5, 1)
        layout1.addWidget(self.humadity_lineedit, 6, 1)

        self.surface_label = QLabel("Surface materials")
        self.walls_label = QLabel("Walls")
        self.walls = QComboBox()
        self.walls.setEditable(False)
        self.walls.addItems(["anechoic", "hard surface", "brickwork"])
        self.walls.currentTextChanged.connect(self.wall_material_changed)

        self.floor_label = QLabel("Floor")
        self.floor = QComboBox()
        self.floor.setEditable(False)
        self.floor.addItems(["brickwork", "stage floor"])
        self.floor.currentTextChanged.connect(self.floor_material_changed)

        layout1.addWidget(self.surface_label, 7, 0)
        layout1.addWidget(self.walls_label, 8, 0)
        layout1.addWidget(self.walls, 8, 1)

        layout1.addWidget(self.floor_label, 9, 0)
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


    def wall_material_changed(self, material):
        print(material)

    def floor_material_changed(self, material):
        print(material)


class SimulationParametersWindow(QWidget):
    def __init__(self):
        super(SimulationParametersWindow, self).__init__()
        self.setWindowTitle("Simulation parameters")
        self.setGeometry(150, 80, 350, 400)

        layout = QVBoxLayout()
        layout1 = QGridLayout()
        layout2 = QHBoxLayout()

        self.fs_label = QLabel("Sampling frequency")
        self.max_order_label = QLabel("Max order")
        self.rt60_label = QLabel("Reverberation time (RT60)")
        self.absorbtion_label = QLabel("Air absorbtion")
        self.ray_tracing_label = QLabel("Ray tracing")
        self.ref_mic_label = QLabel("Reference microphone")
        self.snr_label = QLabel("SNR")

        self.fs_lineedit = QLineEdit()
        self.max_order_lineedit = QLineEdit()
        self.rt60_lineedit = QLineEdit()
        self.absorbtion = QCheckBox()
        self.absorbtion.setCheckable(True)
        self.absorbtion.stateChanged.connect(self.show_state)
        self.ray_tracing = QCheckBox()
        self.ray_tracing.setCheckable(True)
        self.ray_tracing.stateChanged.connect(self.show_state)
        self.ref_mic_lineedit = QLineEdit()
        self.snr_lineedit = QLineEdit()

        layout1.addWidget(self.fs_label, 0, 0)
        layout1.addWidget(self.fs_lineedit, 0, 1)
        layout1.addWidget(self.max_order_label, 1, 0)
        layout1.addWidget(self.max_order_lineedit, 1, 1)
        layout1.addWidget(self.rt60_label, 2, 0)
        layout1.addWidget(self.rt60_lineedit, 2, 1)
        layout1.addWidget(self.absorbtion_label, 3, 0)
        layout1.addWidget(self.absorbtion, 3, 1)
        layout1.addWidget(self.ray_tracing_label, 4, 0)
        layout1.addWidget(self.ray_tracing, 4, 1)
        layout1.addWidget(self.ref_mic_label, 5, 0)
        layout1.addWidget(self.ref_mic_lineedit, 5, 1)
        layout1.addWidget(self.snr_label, 6, 0)
        layout1.addWidget(self.snr_lineedit, 6, 1)


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

    def show_state(self, state):
        print(state == Qt.Checked)
        print(state)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()

