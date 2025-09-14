from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit
from PySide6.QtGui import QFont, Qt, QIcon
from PySide6.QtCore import Signal

from collections.abc import Callable
from threading import Event

CONST_DEFAULT_TIME_LIMIT = "00:04:00" # 4 minutes

class TimerUI(QMainWindow):

    update_timer_signal = Signal(int)

    def __init__(self, stop_event: Event, resource_path_callback: Callable[[str], str], start_timer_callback: Callable[[int, "TimerUI"], None]):
        super().__init__()

        self.update_timer_signal.connect(self.update_timer)

        self.start_timer = start_timer_callback
        self.stop_event = stop_event
        
        self.setWindowTitle("Timer UI")
        alarm_icon = resource_path_callback('res/alarm.ico')
        self.setWindowIcon(QIcon(alarm_icon))
        self.resize(400, 200)
        self.data_fields: dict[str, QLineEdit] = {"Time Limit": QLineEdit(), "Timer": QLineEdit()}

        self.build_ui()

    def build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        font_label = QFont("Arial", 11)
        font_edit = QFont("Arial", 11)

        # Data fields
        layout_data = QHBoxLayout()
        for name, edit in self.data_fields.items():
            h_layout = QVBoxLayout()
            label = QLabel(name)
            label.setFont(font_label)
            edit.setFont(font_edit)
            if name == "Timer":
                edit.setReadOnly(True)

            if name == "Timer":
                edit.setText("00:00:00")
            elif name == "Time Limit":
                edit.setText(CONST_DEFAULT_TIME_LIMIT)

            edit.setFixedHeight(25)
            edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
            h_layout.addWidget(label)
            h_layout.addWidget(edit)
            layout_data.addLayout(h_layout)

        main_layout.setContentsMargins(30, 30, 30, 30)
        layout_data.setSpacing(15)

        main_layout.addLayout(layout_data)

        # Start/Stop Timer button
        self.start_timer_button = QPushButton("Start Timer")
        self.start_timer_button.setFixedHeight(35)
        self.start_timer_button.setFont(QFont("Arial", 11))
        self.start_timer_button.clicked.connect(self.change_timer_status)

        main_layout.addStretch()
        main_layout.addWidget(self.start_timer_button)

        central_widget.setLayout(main_layout)

    def change_timer_status(self):
        if self.start_timer_button.text() == "Start Timer":
            time_limit = self.data_fields["Time Limit"].text()

            try:
                h, m, s = map(int, time_limit.split(":")) # Expecting format HH:MM:SS and saves hours, minutes and seconds in variables mapping them from time_limit variable
            except ValueError:
                print("Invalid time format. Please use HH:MM:SS.")
                self.start_timer_button.setText("Start Timer")
                return
            time_limit = h * 3600 + m * 60 + s

            print("Starting timer...")
            self.stop_event.clear()
            self.start_timer_button.setText("Stop Timer")
            self.data_fields["Time Limit"].setReadOnly(True)
            self.start_timer(time_limit, self)
        else:
            print("Stopping timer...")
            self.data_fields["Time Limit"].setReadOnly(False)
            self.start_timer_button.setText("Start Timer")
            self.stop_event.set()

    def update_timer(self, seconds: int):
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        h = str(h).rjust(2, '0')
        m = str(m).rjust(2, '0')
        s = str(s).rjust(2, '0')

        self.data_fields["Timer"].setText(f"{h}:{m}:{s}")