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
)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle('My app')
        geometry = app.desktop().availableGeometry()
        self.setGeometry(geometry)

        self.source_window = SourceWindow()

        room_pic = QLabel()
        souunsin_pic = QLabel()
        micsin_pic = QLabel()
        sources_pic = QLabel()
        mics_pic = QLabel()

        room_pic.setPixmap(QPixmap('room_graphics.jpg'))
        souunsin_pic.setPixmap(QPixmap('sound_sin.jpg'))
        micsin_pic.setPixmap(QPixmap('mic_sin.jpg'))
        sources_pic.setPixmap(QPixmap('sources.jpg'))
        mics_pic.setPixmap(QPixmap('mics.jpg'))

        layout = QHBoxLayout()
        layout_mic_sources_player = QVBoxLayout()
        layout_room_sins = QVBoxLayout()

        layout_mic_sources_player.addWidget(sources_pic)
        layout_mic_sources_player.addWidget(mics_pic)
        layout_mic_sources_player.addWidget(QLabel("PLAYER"))
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
        room_action.triggered.connect(self.onMenuBarFileClick)
        source_action = QAction("Source", self)
        source_action.triggered.connect(self.show_Sources_window)
        mic_action = QAction("Microphone", self)
        mic_action.triggered.connect(self.onMenuBarFileClick)
        simparams_action = QAction("Simulation parameters", self)
        simparams_action.triggered.connect(self.onMenuBarFileClick)

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


class SourceWindow(QWidget):
    def __init__(self):
        super(SourceWindow, self).__init__()
        self.setWindowTitle("Sources")
        self.setGeometry(150, 80, 500, 350)

        layout = QGridLayout()


        self.sources = QComboBox()
        self.sources.setEditable(True)  # to add sources
        self.sources.addItems(["Source1", "Source2", "Add Source"])
        self.sources.currentIndexChanged.connect(self.source_index_changed)
        self.sources.currentTextChanged.connect(self.sources_text_changed)
        # QComboBox.InsertBeforeCurrent- insert will be handled like this - Insert before current item(before add source item)
        self.sources.setInsertPolicy(QComboBox.InsertBeforeCurrent)

        self.func_radiobtn = QRadioButton("Functional")
        self.func_radiobtn.setChecked(True)
        self.file_radiobtn = QRadioButton("Wav file")
        #self.file_radiobtn.setChecked(True)

        layout.addWidget(self.sources, 0, 0)
        layout.addWidget(self.func_radiobtn, 1, 0)
        layout.addWidget(self.file_radiobtn, 1, 1)

        self.mute_box = QCheckBox("Mute")
        self.mute_box.setCheckable(True)
        self.mute_box.stateChanged.connect(self.show_state)
        self.rmmove_box = QCheckBox("Remove")
        self.rmmove_box.setCheckable(True)
        self.rmmove_box.stateChanged.connect(self.show_state)

        layout.addWidget(self.mute_box, 0, 2)
        layout.addWidget(self.rmmove_box, 0, 3)

        self.position_label = QLabel("Position")
        self.x_pos_line_edit = QLineEdit()
        self.x_pos_line_edit.setPlaceholderText("X coordinate")
        self.y_pos_line_edit = QLineEdit()
        self.y_pos_line_edit.setPlaceholderText("Y coordinate")
        self.z_pos_line_edit = QLineEdit()
        self.z_pos_line_edit.setPlaceholderText("Z coordinate")

        layout.addWidget(self.position_label, 2, 0)
        layout.addWidget(self.x_pos_line_edit, 2, 1)
        layout.addWidget(self.y_pos_line_edit, 2, 2)
        layout.addWidget(self.z_pos_line_edit, 2, 3)

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

        layout.addWidget(self.amplitude_label, 3, 0)
        layout.addWidget(self.amp_line_edit, 3, 1)
        layout.addWidget(self.frequency_label, 4, 0)
        layout.addWidget(self.freq_line_edit, 4, 1)
        layout.addWidget(self.fs_label, 5, 0)
        layout.addWidget(self.fs_line_edit, 5, 1)
        layout.addWidget(self.phase_label, 3, 2)
        layout.addWidget(self.phase_line_edit, 3, 3)
        layout.addWidget(self.time_label, 4, 2)
        layout.addWidget(self.time_line_edit, 4, 3)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setStyleSheet("color: white;")
        self.btn_ok.setStyleSheet("Background-color: grey;")
        self.btn_apply = QPushButton("Apply")
        self.btn_apply.setStyleSheet("Background-color: grey;")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setStyleSheet("Background-color: grey;")

        layout.addWidget(self.btn_apply, 6, 1)
        layout.addWidget(self.btn_cancel, 6, 2)
        layout.addWidget(self.btn_ok, 6, 3)

        self.setLayout(layout)

    def source_index_changed(self, index):
        print("Source", index)

    def sources_text_changed(self, text):
        print(text)

    def show_state(self, state):
        print(s == Qt.Checked)
        print(s)




app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()




