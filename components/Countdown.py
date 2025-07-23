import math
from typing import Callable

import customtkinter as ctk

from styles.colors import COLORS
from styles.progress import (
    PROGRESS_EMPTY_STYLES,
    PROGRESS_ORANGE_STYLES,
    PROGRESS_RED_STYLES,
    PROGRESS_YELLOW_STYLES,
)

TimerCallback = Callable[[], None]


def get_time_label_color(ratio: float):
    if ratio > 2 / 3:
        return COLORS["YELLOW"]
    elif ratio > 1 / 3:
        return COLORS["ORANGE"]
    else:
        return COLORS["RED"]


def get_progress_bar_color(ratio: float):
    if ratio > 2 / 3:
        return PROGRESS_YELLOW_STYLES
    elif ratio > 1 / 3:
        return PROGRESS_ORANGE_STYLES
    elif ratio == 0:
        return PROGRESS_EMPTY_STYLES
    else:
        return PROGRESS_RED_STYLES


class Countdown(ctk.CTkFrame):
    def __init__(
        self,
        master,
        default_time=30,
        on_begin: TimerCallback | None = None,
        on_end: TimerCallback | None = None,
        **kwargs,
    ):
        super().__init__(master, **kwargs)

        self.max_seconds = default_time
        self.remaining_seconds = default_time

        self._on_begin = on_begin
        self._on_end = on_end

        self._tick_timer_handle = ""

        self._create_widgets()

    def _create_widgets(self):
        from styles import font as FONT

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.time_label = time_label = ctk.CTkLabel(
            self,
            font=FONT.Font80Bold,
            text=str(self.remaining_seconds),
            anchor="center",
            text_color=get_time_label_color(self.remaining_seconds / self.max_seconds),
        )
        time_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.time_progress_bar = time_progress_bar = ctk.CTkProgressBar(
            self,
            orientation="vertical",
            width=20,
            determinate_speed=0.1,
            **get_progress_bar_color(self.remaining_seconds / self.max_seconds),
        )
        time_progress_bar.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        self.button = button = ctk.CTkButton(
            self,
            text="จับเวลา",
            command=self._toggle_timer,
            font=FONT.Font16,
            height=32,
            width=0,
        )
        button.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def _update_widgets(self):
        time_ratio = self.remaining_seconds / self.max_seconds
        self.time_label.configure(
            text=math.ceil(self.remaining_seconds),
            text_color=get_time_label_color(time_ratio),
        )
        self.time_progress_bar.configure(**get_progress_bar_color(time_ratio))
        self.time_progress_bar.set(time_ratio)

    def set_time(self, time: int):
        self._cancel_job()

        self.max_seconds = time

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

        if self._on_begin:
            self._on_begin()

    def _reset_timer(self):
        self._cancel_job()

        self.button.configure(text="จับเวลา")

        self.remaining_seconds = self.max_seconds
        self._update_widgets()

        if self._on_end:
            self._on_end()

    def _schedule_job(self):
        self._tick_timer_handle = self.after(100, self._tick)

    def _cancel_job(self):
        if self._tick_timer_handle:
            self.after_cancel(self._tick_timer_handle)
            self._tick_timer_handle = ""

    def _tick(self):
        self.remaining_seconds = (self.remaining_seconds * 10 - 1) / 10
        self._update_widgets()
        if self.remaining_seconds:
            self._schedule_job()
        else:
            # TODO - Play sound
            self._cancel_job()
