import random
from typing import Literal

import customtkinter as ctk
import ttkbootstrap as ttk
from PIL import ImageTk

from components.Countdown import Countdown
from components.Digits import Digits
from interface import AppInterface, RoundOptions
from utils.logo import update_logo_in_frame
from windows.Option import OptionWindow

# from utils.validation import validate_positive_number
# import ttkbootstrap.constants as tc
# import ttkbootstrap.validation as tv

ctk.set_appearance_mode("Light")


class App(ttk.Window, AppInterface):
    def __init__(self):
        super().__init__()

        self.style.load_user_themes("./theme.json")
        self.style.theme_use("nsru")

        self.title("โปรแกรมคิดเลขเร็ว — Fastmath")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.place_window_center()

        self._event_name = "โปรแกรมคิดเลขเร็ว"
        self._histories = ttk.StringVar(self, "ประวัติโจทย์\n")
        self._round_options = [
            RoundOptions(
                question_count=10,
                time_per_question=30,
                question_digit=4,
                answer_digit=2,
                highlighted_question_digits=set()
            ),
            RoundOptions(
                question_count=10,
                time_per_question=30,
                question_digit=4,
                answer_digit=2,
                highlighted_question_digits=set()
            ),
            RoundOptions(
                question_count=10,
                time_per_question=30,
                question_digit=4,
                answer_digit=2,
                highlighted_question_digits=set()
            ),
            RoundOptions(
                question_count=10,
                time_per_question=30,
                question_digit=4,
                answer_digit=2,
                highlighted_question_digits=set()
            ),
        ]


        self._spin_problem_timer_handle = ''
        self._spin_answer_timer_handle = ''

        self._create_widgets()
        # self.open_option_window()

    def _create_widgets(self):
        # self.style.configure("TLabel", font=("Anuphan"))
        # self.style.configure("TButton", font=("Anuphan"))
        self.style.configure("Large.warning.TButton", font=(None, 24))
        self.style.configure("Large.success.TButton", font=(None, 24))
        self.style.configure("Medium.TButton", font=(None, 16))
        self.style.configure("bglight.TButton", background="#ebf1fc")
        self.style.configure("display.light.Inverse.TLabel", background="#fff")
        self.style.configure("lighter.light.TFrame", background="#f9ffff")
        self.style.configure(
            "dark.TEntry", background="#ebf1fc", fieldbackground="#f9ffff"
        )

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew")
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # --- LEFT SIDE ---
        event_title_area = ttk.Frame(left_frame)
        event_title_area.pack(fill="x", padx=(10, 0), pady=(10, 0))

        self.image_references: list[ImageTk.PhotoImage] = []

        self._event_logo_frame = ttk.Frame(event_title_area, style="light.TFrame")
        self._event_logo_frame.pack(side="left", fill="both")

        self._event_name_label = event_name_label = ttk.Label(
            event_title_area,
            text=self._event_name,
            font=("Arial", 16),
            anchor="e",
        )
        event_name_label.pack(side="right", fill="both", expand=True)

        problem_frame = ttk.Frame(left_frame, padding=10, style="light.TFrame")
        problem_frame.pack(fill="both", padx=(10, 0), pady=(10, 5), expand=True)

        self._problem_frame = problem_center_frame = Digits(problem_frame)
        problem_center_frame.pack(expand=True)

        # TODO - สุ่ม math.random() ต่อ digit ได้เลย ไม่ต้องอ้างอิงกฎ
        problem_center_frame.set_digits([0] * 4)

        answer_frame = ttk.Frame(left_frame, padding=10, style="light.TFrame")
        answer_frame.pack(fill="both", padx=(10, 0), pady=(5, 10), expand=True)

        self._answer_frame = answer_center_frame = Digits(answer_frame)
        answer_center_frame.pack(expand=True)

        answer_center_frame.set_digits([0] * 2)

        # --- RIGHT SIDE ---
        ttk.Label(right_frame, text="Powered by Fastmath.io", anchor="e").pack(
            fill="x", pady=(10, 8), padx=10
        )

        round_frame = ttk.Frame(right_frame, padding=10, style="light.TFrame")
        round_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            round_frame,
            text="รอบที่ 1 ข้อที่ 1",
            font=("Arial", 16),
            anchor="center",
            style="light.Inverse.TLabel",
        ).pack(fill="x")

        cnt = Countdown(
            right_frame,
            30,
            on_begin=self._on_countdown_begin,
            on_end=self._on_countdown_end
        )
        cnt.pack(fill="both", padx=10, expand=True)

        action_frame = ttk.Frame(right_frame, padding=10, style="light.TFrame")
        action_frame.pack(fill="x", padx=10, pady=10)

        self._get_question_btn = get_question_btn = ttk.Button(
            action_frame,
            text="สุ่มโจทย์",
            padding=10,
            style="Large.warning.TButton",
            command=self._spin_problem,
        )
        get_question_btn.pack(fill="x")

        self._get_answer_btn = get_answer_btn = ttk.Button(
            action_frame,
            text="สุ่มคำตอบ",
            padding=10,
            style="Large.success.TButton",
            command=self._spin_answer,
        )
        get_answer_btn.pack(fill="x", pady=10)

        action_ext_frame = ttk.Frame(action_frame, style="light.TFrame")
        action_ext_frame.pack(fill="x")

        action_ext_frame.columnconfigure(1, weight=1)

        self._prev_btn = prev_btn = ttk.Button(action_ext_frame, text="⬅︎", style="bglight.TButton")
        prev_btn.grid(row=0, column=0, sticky="w")

        self._next_btn = next_btn = ttk.Button(action_ext_frame, text="ข้อถัดไป", style="bglight.TButton")
        next_btn.grid(row=0, column=1, sticky="ew", padx=10)

        self._config_btn = config_btn = ttk.Button(
            action_ext_frame,
            text="⚙️",
            style="bglight.TButton",
            command=self.open_option_window,
        )
        config_btn.grid(row=0, column=2, sticky="e")

        # countdown_seconds = ttk.StringVar(value="30")

        # spin = ttk.Spinbox(left_frame, textvariable=countdown_seconds, from_=1, to=60)
        # spin.pack()
        # tv.add_validation(spin, validate_positive_number, "key")

        # def handle_spin(*args):
        #     if x := countdown_seconds.get():
        #         try:
        #             cnt.set_time(int(x))
        #         except ValueError:
        #             pass

        # countdown_seconds.trace_add("write", handle_spin)

    def _spin_problem(self):
        if self._spin_problem_timer_handle:
            self.after_cancel(self._spin_problem_timer_handle)

        digits = [random.randint(0, 9) for _ in range(4)]

        def after_spin():
            self._problem_frame.stop_spinning()
            self._problem_frame.set_digits(digits)

        self._problem_frame.start_spinning()

        self._spin_problem_timer_handle = self.after(1500, after_spin)

    def _spin_answer(self):
        if self._spin_answer_timer_handle:
            self.after_cancel(self._spin_answer_timer_handle)

        digits = [random.randint(0, 9) for _ in range(2)]

        def after_spin():
            self._answer_frame.stop_spinning()
            self._answer_frame.set_digits(digits)

        self._answer_frame.start_spinning()

        self._spin_answer_timer_handle = self.after(1500, after_spin)

    def _on_countdown_begin(self):
        self._get_question_btn['state'] = 'disabled'
        self._get_answer_btn['state'] = 'disabled'
        self._prev_btn['state'] = 'disabled'
        self._next_btn['state'] = 'disabled'
        self._config_btn['state'] = 'disabled'

    def _on_countdown_end(self):
        self._get_question_btn['state'] = 'normal'
        self._get_answer_btn['state'] = 'normal'
        self._prev_btn['state'] = 'normal'
        self._next_btn['state'] = 'normal'
        self._config_btn['state'] = 'normal'

    def open_option_window(self):
        window = OptionWindow(self)
        window.grab_set()

    def update_logo(self, filepaths: tuple[str, ...] | Literal[""]):
        update_logo_in_frame(filepaths, self._event_logo_frame, self.image_references)

    @property
    def festname(self) -> str:
        return self._event_name

    @festname.setter
    def festname(self, value: str):
        self._event_name = value
        self._event_name_label["text"] = value

    @property
    def history(self) -> ttk.StringVar:
        return self._histories

    @property
    def round_options(self) -> list[RoundOptions]:
        return self._round_options


if __name__ == "__main__":
    app = App()
    app.mainloop()
