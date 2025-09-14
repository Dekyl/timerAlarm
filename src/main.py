from threading import Thread
import threading, time, sys, os

from PySide6.QtWidgets import QApplication

from ui import TimerUI

stop_event = threading.Event()

class TimerLogic:

    def __init__(self, time_limit: int, ui: TimerUI):
        self.ui = ui
        self.time_limit = time_limit
        self.elapsed_time = 0

    def run_timer(self):
        while not stop_event.is_set():
            if self.elapsed_time >= self.time_limit:
                self.elapsed_time = 0
                self.ui.update_timer_signal.emit(self.elapsed_time)

            time.sleep(1)
            self.elapsed_time += 1
            self.ui.update_timer_signal.emit(self.elapsed_time)

        self.elapsed_time = 0
        self.ui.update_timer_signal.emit(self.elapsed_time)

def resource_path(relative_path: str) -> str:
    if hasattr(sys, '_MEIPASS'):
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def start_timer(time_limit: int, ui: TimerUI):
    timer_logic = Thread(target=lambda: TimerLogic(
        time_limit, 
        ui
    ).run_timer())
    timer_logic.start()

def main():
    app = QApplication(sys.argv)
    ui = TimerUI(stop_event, resource_path, start_timer)
    ui.show()
    app.exec()

if __name__ == "__main__":
    main()