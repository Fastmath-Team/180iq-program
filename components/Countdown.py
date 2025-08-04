import math
from typing import Callable

import customtkinter as ctk
import pygame.mixer

from styles import colors as COLORS
from utils.file import get_file

TimerCallback = Callable[[], None]


def interpolate_color(color1_rgb: tuple, color2_rgb: tuple, factor: float) -> str:
    r = int(color1_rgb[0] + factor * (color2_rgb[0] - color1_rgb[0]))
    g = int(color1_rgb[1] + factor * (color2_rgb[1] - color1_rgb[1]))
    b = int(color1_rgb[2] + factor * (color2_rgb[2] - color1_rgb[2]))
    return f"#{r:02x}{g:02x}{b:02x}"


def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


GREEN_RGB = hex_to_rgb(COLORS.Green)
YELLOW_RGB = hex_to_rgb(COLORS.Yellow)
RED_RGB = hex_to_rgb(COLORS.Red)


def get_color_from_ratio(ratio: float):
    ratio = max(0.0, min(1.0, ratio))
    if ratio > 0.5:
        factor = (1.0 - ratio) * 2
        return interpolate_color(GREEN_RGB, YELLOW_RGB, factor)
    else:
        factor = (0.5 - ratio) * 2
        return interpolate_color(YELLOW_RGB, RED_RGB, factor)


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

        pygame.mixer.init(44100, -16, 2, 2048)
        self.sound = pygame.mixer.Sound(get_file("assets/ding.mp3"))
        self.sound.set_volume(1)

        self.max_seconds = default_time
        self.remaining_seconds = default_time

        self._on_begin = on_begin
        self._on_end = on_end

        self._tick_timer_handle = ""

        self._create_widgets()

    def _create_widgets(self):
        from styles import font as FONT

        self.columnconfigure(0, weight=5)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)

        # เพิ่มตัวเลข "00" แบบคงที่เข้ามาในหน้าต่าง
        # ตัวเลขนี้จะถูกซ้อนอยู่ด้านหลังตัวเลขจับเวลา
        self.static_background_label = ctk.CTkLabel(
            self,
            font=FONT.Font80Bold,
            text="00",
            anchor="center",
            text_color="#FFFFFF",  # กำหนดเป็นสีขาว
        )
        self.static_background_label.grid(
            row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew"
        )

        self.time_label = time_label = ctk.CTkLabel(
            self,
            font=FONT.Font80Bold,
            text=str(self.remaining_seconds),
            anchor="center",
            text_color=get_color_from_ratio(self.remaining_seconds / self.max_seconds),
        )
        time_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.time_progress_bar = time_progress_bar = ctk.CTkProgressBar(
            self, orientation="vertical", corner_radius=0, determinate_speed=0.1
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
            text_color=get_color_from_ratio(time_ratio),
        )
        if self.remaining_seconds > 0:
            if not self.time_progress_bar.winfo_ismapped():
                self.time_progress_bar.grid(
                    row=0, column=1, padx=10, pady=(10, 0), sticky="nsew"
                )
            self.time_progress_bar.configure(
                progress_color=get_color_from_ratio(time_ratio), fg_color="#ffffff"
            )
            self.time_progress_bar.set(time_ratio)
        else:
            self.time_progress_bar.set(0)

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
            if self.sound:
                self.sound.play()
            self._cancel_job()
