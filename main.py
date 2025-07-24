import math
import platform
import random
import tkinter as tk
from bisect import bisect_right

import customtkinter as ctk
from PIL import Image

from components.Countdown import Countdown
from components.Digits import Digits
from interface import AppInterface, QuestionAnswer, Round, RoundOptions
from styles.theme import THEME
from utils.file import get_file
from utils.logo import update_logo_in_frame
from utils.responsive import get_responsive_value_from_width
from windows.Option import OptionWindow

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme(get_file("styles/theme.json"))

VERSION = "1.0.0"


class App(ctk.CTk, AppInterface):
    def __init__(self):
        super().__init__()

        self.title("โปรแกรมคิดเลขเร็ว — Fastmath")
        self.geometry("800x600")
        self.minsize(800, 600)
        if platform.system() == "Windows":
            self.iconbitmap(get_file("assets/icon.ico"))
        self.iconphoto(True, tk.PhotoImage(file=get_file("assets/icon.png")))

        self._event_name = "โปรแกรมคิดเลขเร็ว"
        self._event_logo_files: tuple[str, ...] = tuple()
        self._rounds: list[Round] = [
            Round(
                items=[],
                options=RoundOptions(
                    question_count=10,
                    time_per_question=30,
                    question_digit=4,
                    answer_digit=2,
                    highlighted_question_digits=set(),
                ),
            ),
        ]

        self._current_index = 0
        self._current_round_index = 0
        self._current_last = False

        self._spin_problem_timer_handle = ""
        self._spin_answer_timer_handle = ""

        self._create_widgets()

        self.trigger_update_rounds("all")

        self._current_breakpoint = 0
        self.bind("<Configure>", self.on_window_resize)
        self.on_window_resize(None)

    def _create_widgets(self):
        from styles import font as FONT

        self.__FONT__ = FONT

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(self, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame = ctk.CTkFrame(self, fg_color="transparent", width=0)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # --- LEFT SIDE ---
        event_title_area = ctk.CTkFrame(left_frame, fg_color="transparent")
        event_title_area.pack(fill="x", padx=(10, 0), pady=(10, 0))

        self.image_references: list[ctk.CTkImage] = []

        self._event_name_label = event_name_label = ctk.CTkLabel(
            event_title_area,
            text=self._event_name,
            font=FONT.Font16Bold,
            anchor="w",
            text_color=THEME.CTkFrame.fg_color[0],
        )
        event_name_label.pack(side="left", fill="both", expand=True)

        self._event_logo_frame = ctk.CTkFrame(
            event_title_area, corner_radius=0, fg_color="transparent", height=24
        )
        self._event_logo_frame.pack(side="right", fill="both")

        problem_frame = ctk.CTkFrame(left_frame)
        problem_frame.pack(fill="both", padx=(10, 0), pady=(10, 5), expand=True)

        self._problem_frame = problem_center_frame = Digits(problem_frame)
        problem_center_frame.pack(expand=True)

        answer_frame = ctk.CTkFrame(left_frame)
        answer_frame.pack(fill="both", padx=(10, 0), pady=(5, 10), expand=True)

        self._answer_frame = answer_center_frame = Digits(answer_frame, mode="compact")
        answer_center_frame.pack(expand=True)

        # --- RIGHT SIDE ---
        self._fastmath_logo = fastmath_logo = ctk.CTkImage(
            light_image=Image.open(get_file("assets/logo.png")), size=(145, 24)
        )
        ctk.CTkLabel(right_frame, text="", anchor="e", image=fastmath_logo).pack(
            fill="x", pady=(10, 0), padx=10
        )

        round_frame = ctk.CTkFrame(right_frame)
        round_frame.pack(fill="x", padx=10, pady=10)

        self._round_question_label = round_question_label = ctk.CTkLabel(
            round_frame, text="รอบที่ 1 ข้อที่ 1", font=FONT.Font24, padx=10, pady=10
        )
        round_question_label.pack(fill="x", padx=10)

        self._cnt = cnt = Countdown(
            right_frame,
            30,
            on_begin=self._on_countdown_begin,
            on_end=self._on_countdown_end,
        )
        cnt.pack(fill="both", padx=10, expand=True)

        action_frame = ctk.CTkFrame(right_frame)
        action_frame.pack(fill="x", padx=10, pady=10)

        self._get_question_btn = get_question_btn = ctk.CTkButton(
            action_frame,
            text="สุ่มโจทย์",
            command=self._on_spin_problem,
            width=0,
            height=56,
            font=FONT.Font24,
        )
        get_question_btn.pack(fill="x", padx=10, pady=(10, 0))

        self._get_answer_btn = get_answer_btn = ctk.CTkButton(
            action_frame,
            text="สุ่มคำตอบ",
            command=self._on_spin_answer,
            width=0,
            height=56,
            font=FONT.Font24,
        )
        get_answer_btn.pack(fill="x", padx=10, pady=10)

        action_ext_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        action_ext_frame.pack(fill="x", padx=10, pady=(0, 10))

        action_ext_frame.columnconfigure(1, weight=1)

        self._prev_btn = prev_btn = ctk.CTkButton(
            action_ext_frame,
            text="⬅︎",
            command=self._on_prev_round,
            width=0,
            font=FONT.Font13,
        )
        prev_btn.grid(row=0, column=0, sticky="w")

        self._next_btn = next_btn = ctk.CTkButton(
            action_ext_frame,
            text="ข้อถัดไป",
            command=self._on_next_round,
            width=0,
            font=FONT.Font13,
        )
        next_btn.grid(row=0, column=1, sticky="ew", padx=10)

        self._config_btn = config_btn = ctk.CTkButton(
            action_ext_frame,
            text="⚙️",
            command=self._on_open_option_window,
            width=0,
            font=FONT.Font13,
        )
        config_btn.grid(row=0, column=2, sticky="e")

    def _on_spin_problem(self):
        if self._spin_problem_timer_handle:
            self.after_cancel(self._spin_problem_timer_handle)

        digits = [
            str(random.randint(0, 9))
            for _ in range(
                self._rounds[self._current_round_index].options.question_digit
            )
        ]

        def after_spin():
            self._problem_frame.stop_spinning()
            self._problem_frame.set_digits(digits)

        self._problem_frame.start_spinning()

        self._spin_problem_timer_handle = self.after(1500, after_spin)

    def _on_spin_answer(self):
        if self._spin_answer_timer_handle:
            self.after_cancel(self._spin_answer_timer_handle)

        digits = [
            str(random.randint(0, 9))
            for _ in range(self._rounds[self._current_round_index].options.answer_digit)
        ]

        def after_spin():
            self._answer_frame.stop_spinning()
            self._answer_frame.set_digits(digits)

        self._answer_frame.start_spinning()

        self._spin_answer_timer_handle = self.after(1500, after_spin)

    def _on_prev_round(self):
        self.current_last = False

        if self._current_index > 0:
            self._current_index -= 1
        elif self._current_round_index > 0:
            self._current_round_index -= 1
            self._current_index = (
                self._rounds[self._current_round_index].options.question_count - 1
            )

            self.trigger_update_rounds("all")

        self._calc_indexes()

    def _on_next_round(self):
        p = self._current_index
        r = self._rounds[self._current_round_index]
        o = r.options
        i = r.items

        prev_last = self.current_last

        if self._current_index < o.question_count - 1:
            self._current_index += 1
        elif self._current_round_index < len(self._rounds) - 1:
            self._current_round_index += 1
            self._current_index = 0
        elif not prev_last:
            self.current_last = True
        else:
            return

        i.insert(
            bisect_right(i, p, key=lambda x: x.index),
            QuestionAnswer(
                p,
                self._problem_frame.get_digits(),
                self._answer_frame.get_digits(),
                o.time_per_question,
                set(o.highlighted_question_digits),
            ),
        )

        if not prev_last and self.current_last:
            return

        self.trigger_update_rounds("all")
        self._calc_indexes()

    def _calc_indexes(self):
        base = sum(
            (
                entry.options.question_count
                for entry in self._rounds[: self._current_round_index]
            )
        )

        self._round_question_label.configure(
            text=f"รอบที่ {self._current_round_index + 1} ข้อที่ {base + self._current_index + 1}"
        )

    def _on_countdown_begin(self):
        self._get_question_btn.configure(state="disabled")
        self._get_answer_btn.configure(state="disabled")
        self._prev_btn.configure(state="disabled")
        self._next_btn.configure(state="disabled")
        self._config_btn.configure(state="disabled")

    def _on_countdown_end(self):
        self._get_question_btn.configure(state="normal")
        self._get_answer_btn.configure(state="normal")
        self._prev_btn.configure(state="normal")
        self._next_btn.configure(state="normal")
        self._config_btn.configure(state="normal")

    def _on_open_option_window(self):
        window = OptionWindow(self)
        window.grab_set()

    def get_logo_height(self) -> int:
        return get_responsive_value_from_width(self.winfo_width(), (24, 38, 48, 62))

    def update_logo(self, size):
        _size = size or self.get_logo_height()
        self._event_logo_frame.configure(height=_size)
        update_logo_in_frame(
            self._event_logo_files,
            self._event_logo_frame,
            self.image_references,
            padx=(10, 0),
            size=_size,
        )

    def on_window_resize(self, event):
        current_width = self.winfo_width()

        width_index = get_responsive_value_from_width(current_width, (0, 1, 2, 3))

        # Skip unnecessary updates
        if width_index == self._current_breakpoint:
            return

        self._current_breakpoint = width_index

        self.__FONT__.update_font_size(current_width)

        logo_size = self.get_logo_height()
        self._fastmath_logo.configure(size=(math.ceil(291 / 48 * logo_size), logo_size))
        self.update_logo(logo_size)

    @property
    def version(self):
        return VERSION

    @property
    def logo_filepaths(self):
        return self._event_logo_files

    @logo_filepaths.setter
    def logo_filepaths(self, filepaths: tuple[str, ...]):
        self._event_logo_files = filepaths

    @property
    def festname(self) -> str:
        return self._event_name

    @festname.setter
    def festname(self, value: str):
        self._event_name = value
        self._event_name_label.configure(text=value)

    @property
    def rounds(self):
        return self._rounds

    def trigger_update_rounds(self, which):
        if which in ("question_digit", "all"):
            self._problem_frame.set_digits(
                ["–"] * self._rounds[self._current_round_index].options.question_digit
            )

        if which in ("answer_digit", "all"):
            self._answer_frame.set_digits(
                ["–"] * self._rounds[self._current_round_index].options.answer_digit
            )

        if which in ("highlighted_question_digits", "all"):
            self._problem_frame.set_highlighted_digits(
                self._rounds[
                    self._current_round_index
                ].options.highlighted_question_digits
            )

        if which in ("timer", "all"):
            self._cnt.set_time(
                self._rounds[self._current_round_index].options.time_per_question
            )

    @property
    def current_index(self):
        return self._current_index

    @property
    def current_round_index(self):
        return self._current_round_index

    @property
    def current_last(self) -> bool:
        return self._current_last

    @current_last.setter
    def current_last(self, value: bool):
        self._current_last = value
        self._next_btn.configure(state="disabled" if value else "normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()
