import time
import threading


class Timers:
    def __init__(self):
        self.player_time = 30
        self.time_pause = False
        self.time_up = False
        self.timer_thread = None

    def start_time(self):
        self.timer_thread = threading.Thread(target=self.count_down)
        self.timer_thread.start()

    def count_down(self):
        while self.player_time > 0:
            if not self.time_pause:
                time.sleep(1)
                self.player_time -= 1
            else:
                time.sleep(1)
        self.time_up = True

    def stop_time(self):
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()

    def help_pause_time(self):
        self.time_pause = True

    def help_resume_time(self):
        self.time_pause = False

    def help_add_time(self):
        self.player_time += 30
        print(f"+30 sec!. Current time left {self.player_time}")

    def reset_timer(self):
        self.player_time = 30
        self.time_pause = False
        self.time_up = False
        self.timer_thread = None

    def reset_question_timer(self):
        self.player_time = 30
        print(f"Time reset{self.player_time}")

