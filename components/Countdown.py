import math

import customtkinter as ctk
import ttkbootstrap as ttk


class Countdown(ctk.CTkFrame):
    def __init__(self, master, defaulttime=30, **kwargs):
        super().__init__(master, **kwargs)

        self.max_seconds = defaulttime
        self.remaining_seconds = defaulttime

        self.after_job_id = None

        self._create_widgets()

    def _create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.time_label = time_label = ctk.CTkLabel(
            self,
            font=("Arial", 80, "bold"),
            text=str(self.remaining_seconds),
            anchor="center",
        )
        time_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.time_progress_bar = time_progress_bar = ttk.Floodgauge(
            self,
            orient="vertical",
            maximum=self.max_seconds * 10,
            value=math.ceil(self.remaining_seconds * 10),
            thickness=20,
        )
        time_progress_bar.grid(
            row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew"
        )

        self.button = button = ctk.CTkButton(
            self, text="จับเวลา", command=self._toggle_timer
        )
        button.grid(row=1, column=0, padx=(10, 0), pady=10, sticky="nsew")

    def _update_widgets(self):
        self.time_label.configure(text=str(math.ceil(self.remaining_seconds)))
        self.time_progress_bar["value"] = math.ceil(self.remaining_seconds * 10)

    def set_time(self, time: int):
        self._cancel_job()

        self.max_seconds = time
        self.time_progress_bar["maximum"] = time * 10

        self._reset_timer()

    def _toggle_timer(self):
        if self.remaining_seconds == self.max_seconds:
            self._start_timer()
        else:
            self._reset_timer()

    def _start_timer(self):
        self.button.configure(text="รีเซ็ต")

        self._update_widgets()
        self._schedule_job()

    def _reset_timer(self):
        self._cancel_job()

        self.button.configure(text="จับเวลา")

        self.remaining_seconds = self.max_seconds
        self._update_widgets()

    def _schedule_job(self):
        self.after_job_id = self.after(100, self._tick)

    def _cancel_job(self):
        if self.after_job_id:
            self.after_cancel(self.after_job_id)
            self.after_job_id = None

    def _tick(self):
        self.remaining_seconds = (self.remaining_seconds * 10 - 1) / 10
        self._update_widgets()
        if self.remaining_seconds:
            self._schedule_job()
        else:
            # TODO - Play sound
            self._cancel_job()
