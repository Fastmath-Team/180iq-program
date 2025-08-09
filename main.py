import json
import platform
import random
import tkinter as tk
from bisect import bisect_right
from tkinter import filedialog, messagebox
from typing import Literal

import customtkinter as ctk
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from components.Countdown import Countdown
from components.Digits import Digits
from interface import AppInterface, QuestionAnswer, Round, RoundOptions
from styles.theme import THEME
from utils.builder import PdfBuilder, build_field
from utils.file import get_file
from utils.logo import update_logo_in_frame
from utils.responsive import get_responsive_value_from_width
from windows.Option import OptionWindow

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme(get_file("styles/theme.json"))

VERSION = "1.2.0"

LOGO_SCALE_FACTOR = 1.25
STATIC_LOGOS = (
    get_file("assets/math.png"),
    get_file("assets/sci.png"),
    get_file("assets/nsru.png"),
    get_file("assets/fastmath.png"),
)


class App(ctk.CTk, AppInterface):
    def __init__(self):
        super().__init__()

        self.title("โปรแกรมคิดเลขเร็ว — MathStat NSRU X Fastmath")
        self.geometry("800x600")
        self.minsize(800, 600)

        self.after(10, self.maximize_window)
        self.is_fullscreen = False

        if platform.system() == "Windows":
            self.iconbitmap(get_file("assets/acad10.ico"))

        self._icon_photo_image = tk.PhotoImage(file=get_file("assets/acad10.png"))
        self.iconphoto(True, self._icon_photo_image)

        pdfmetrics.registerFont(
            TTFont(
                "IBMPlexSansThai-Regular",
                get_file("fonts/IBMPlexSansThai-Regular.ttf"),
            )
        )
        pdfmetrics.registerFont(
            TTFont("IBMPlexSansThai-Bold", get_file("fonts/IBMPlexSansThai-Bold.ttf"))
        )
        pdfmetrics.registerFontFamily(
            "IBMPlexSansThai",
            normal="IBMPlexSansThai-Regular",
            bold="IBMPlexSansThai-Bold",
            italic="IBMPlexSansThai-Regular",
            boldItalic="IBMPlexSansThai-Bold",
        )

        # กำหนดค่าเริ่มต้น (default values)
        self._event_name_default = "คณิตศาสตร์วิชาการ ครั้งที่ 10"
        self._event_logo_files_default: tuple[str, ...] = tuple(
            [get_file("assets/acad10logo.png")]
        )
        self._rounds_default: list[Round] = [
            Round(
                items=[],
                options=RoundOptions(
                    question_count=8,
                    time_per_question=30,
                    question_digit=4,
                    answer_digit=2,
                    highlighted_question_digits=set(),
                ),
            ),
            Round(
                items=[],
                options=RoundOptions(
                    question_count=9,
                    time_per_question=30,
                    question_digit=5,
                    answer_digit=3,
                    highlighted_question_digits=set(),
                ),
            ),
            Round(
                items=[],
                options=RoundOptions(
                    question_count=8,
                    time_per_question=40,
                    question_digit=5,
                    answer_digit=3,
                    highlighted_question_digits={0, 1},
                ),
            ),
        ]

        # ใช้ค่าเริ่มต้นทันที
        self._event_name = self._event_name_default
        self._event_logo_files: tuple[str, ...] = self._event_logo_files_default
        self._rounds: list[Round] = self._rounds_default

        self._current_index = 0
        self._current_round_index = 0
        self._current_last = False

        self._spin_problem_timer_handle = ""
        self._spin_answer_timer_handle = ""

        self._create_widgets()

        # Defer initial data loading -> faster first paint
        self.after(100, self._initial_load)

        self._current_breakpoint = 0
        self.bind("<Configure>", self.on_window_resize)
        self.on_window_resize(None)

        self.bind("<F11>", self.toggle_fullscreen)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _initial_load(self):
        self._load_settings()
        self.trigger_update_rounds("all")
        self._calc_indexes()
        self.update_logo(None)

    def maximize_window(self):
        if platform.system() == "Windows":
            self.state("zoomed")
        elif platform.system() == "Darwin":
            # Skip window size animation on macOS
            screen_width = self.winfo_screenwidth()
            screen_height = self.winfo_screenheight()
            self.geometry(f"{screen_width}x{screen_height}+0+0")
        else:
            self.state("zoomed")

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.attributes("-fullscreen", True)
            self.overrideredirect(True)
        else:
            self.overrideredirect(False)
            self.attributes("-fullscreen", False)
            self.maximize_window()

    def save_settings(self):
        settings = {
            "event_name": self.festname,
            "logo_filepaths": list(self.logo_filepaths),
            "rounds": [
                {
                    "options": {
                        "question_count": r.options.question_count,
                        "time_per_question": r.options.time_per_question,
                        "question_digit": r.options.question_digit,
                        "answer_digit": r.options.answer_digit,
                        "highlighted_question_digits": list(
                            r.options.highlighted_question_digits
                        ),
                    }
                }
                for r in self._rounds
            ],
        }
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
        print("Settings saved successfully!")

    def _load_settings(self):
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)

            temp_festname = settings.get("event_name", self._event_name_default)
            temp_logo_filepaths = tuple(
                settings.get("logo_filepaths", self._event_logo_files_default)
            )

            rounds_data = settings.get("rounds", [])
            temp_rounds = (
                [
                    Round(
                        items=[],
                        options=RoundOptions(
                            question_count=r["options"]["question_count"],
                            time_per_question=r["options"]["time_per_question"],
                            question_digit=r["options"]["question_digit"],
                            answer_digit=r["options"]["answer_digit"],
                            highlighted_question_digits=set(
                                r["options"]["highlighted_question_digits"]
                            ),
                        ),
                    )
                    for r in rounds_data
                ]
                if rounds_data
                else []
            )

            self.festname = temp_festname
            self.logo_filepaths = temp_logo_filepaths
            self._rounds = temp_rounds

            print("Settings loaded successfully!")

        except FileNotFoundError:
            print("Settings file not found. Using default settings.")
        except Exception as e:
            print(f"Error loading settings: {e}. Using default settings.")

    def _create_widgets(self):
        from styles import font as FONT

        self.__FONT__ = FONT

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.event_title_area = ctk.CTkFrame(self, fg_color="transparent")
        self.event_title_area.grid(
            row=0, column=0, sticky="nsew", padx=(10, 0), pady=10
        )
        self.event_title_area.grid_columnconfigure(0, weight=1)
        self.image_references: list[ctk.CTkImage] = []

        self._event_name_label = ctk.CTkLabel(
            self.event_title_area,
            text=self.festname,
            font=FONT.Font16Bold,
            anchor="w",
            text_color=THEME.CTkFrame.fg_color[0],
        )
        self._event_name_label.grid(row=0, column=0, sticky="w")

        self._event_logo_frame = ctk.CTkFrame(
            self.event_title_area, corner_radius=0, fg_color="transparent", height=24
        )
        self._event_logo_frame.grid(row=0, column=1, sticky="e")

        main_content_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_content_frame.grid(row=1, column=0, sticky="nsew")

        main_content_frame.grid_columnconfigure(0, weight=20)
        main_content_frame.grid_columnconfigure(1, weight=1)
        main_content_frame.grid_rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.grid_rowconfigure(0, weight=1)
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        problem_frame = ctk.CTkFrame(left_frame)
        problem_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 0), pady=(0, 5))
        problem_frame.grid_columnconfigure(0, weight=1)
        problem_frame.grid_rowconfigure(0, weight=1)

        self._problem_frame = Digits(problem_frame)
        self._problem_frame.pack(expand=True)

        answer_frame = ctk.CTkFrame(left_frame)
        answer_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 0), pady=(5, 10))
        answer_frame.grid_columnconfigure(0, weight=1)
        answer_frame.grid_rowconfigure(0, weight=1)

        self._answer_frame = Digits(answer_frame, mode="compact")
        self._answer_frame.pack(expand=True)

        right_frame = ctk.CTkFrame(main_content_frame, fg_color="transparent")
        right_frame.grid(row=0, column=1, sticky="nsew")

        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        round_label_frame = ctk.CTkFrame(right_frame)
        round_label_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 5))
        round_label_frame.grid_columnconfigure(0, weight=1)

        # Preserve space
        self._round_question_label_bg = ctk.CTkLabel(
            round_label_frame,
            text="รอบที่ 0 ข้อที่ 00",
            font=FONT.Font24,
            text_color="white",
        )
        self._round_question_label_bg.grid(
            row=0, column=0, sticky="nsew", padx=10, pady=(0, 5)
        )

        self._round_question_label = ctk.CTkLabel(
            round_label_frame, text="รอบที่ 1 ข้อที่ 1", font=FONT.Font24
        )
        self._round_question_label.grid(
            row=0, column=0, sticky="nsew", padx=10, pady=(0, 5)
        )

        self._cnt = Countdown(
            right_frame,
            30,
            on_begin=self._on_countdown_begin,
            on_end=self._on_countdown_end,
        )
        self._cnt.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 5))

        action_frame = ctk.CTkFrame(right_frame)
        action_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
        action_frame.columnconfigure(1, weight=1)

        self._get_question_btn = ctk.CTkButton(
            action_frame,
            text="สุ่มโจทย์",
            command=self._on_spin_problem,
            width=0,
            height=56,
            font=FONT.Font24,
        )
        self._get_question_btn.pack(fill="x", padx=10, pady=(10, 0))

        self._get_answer_btn = ctk.CTkButton(
            action_frame,
            text="สุ่มคำตอบ",
            command=self._on_spin_answer,
            width=0,
            height=56,
            font=FONT.Font24,
        )
        self._get_answer_btn.pack(fill="x", padx=10, pady=10)

        action_ext_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        action_ext_frame.pack(fill="x", padx=10, pady=(0, 10))
        action_ext_frame.columnconfigure(1, weight=1)

        self._prev_btn = ctk.CTkButton(
            action_ext_frame,
            text=" ⬅ ",
            command=self._on_prev_round,
            width=0,
            font=FONT.Font13,
        )
        self._prev_btn.grid(row=0, column=0, sticky="w")

        self._next_btn = ctk.CTkButton(
            action_ext_frame,
            text="ข้อถัดไป",
            command=self._on_next_round,
            width=0,
            font=FONT.Font13,
        )
        self._next_btn.grid(row=0, column=1, sticky="ew", padx=10)

        self._config_btn = ctk.CTkButton(
            action_ext_frame,
            text="⚙️",
            command=self._on_open_option_window,
            width=0,
            font=FONT.Font13,
        )
        self._config_btn.grid(row=0, column=2, sticky="e")

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
            str(random.randint(0 if i else 1, 9))
            for i in range(self._rounds[self._current_round_index].options.answer_digit)
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

    def reset_settings(self):
        self.festname = self._event_name_default
        self.logo_filepaths = self._event_logo_files_default
        self._rounds = self._rounds_default
        self.save_settings()

        self.trigger_update_rounds("all")
        self._calc_indexes()
        self.update_logo(None)

    def get_logo_height(self) -> int:
        return get_responsive_value_from_width(self.winfo_width(), (14, 23, 29, 37))

    def update_logo(self, size):
        if size is None:
            size = self.get_logo_height()

        scaled_size = int(size * LOGO_SCALE_FACTOR)

        self._event_logo_frame.configure(height=scaled_size)
        all_logos = (*self.logo_filepaths, *STATIC_LOGOS)

        update_logo_in_frame(
            all_logos,
            self._event_logo_frame,
            self.image_references,
            size=scaled_size,
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
        self.update_logo(logo_size)

    def on_closing(self):
        if self._rounds[0].items:
            result = messagebox.askyesnocancel(
                "ปิดโปรแกรม", "ท่านมีประวัติการเล่นอยู่ ต้องการบันทึกโจทย์หรือไม่?"
            )

            if result is None:
                return
            if result and not self.export_to_pdf("exit"):
                return
        self.destroy()

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

    def export_to_pdf(self, source: Literal["exit", "option"] = "option"):
        if not self._rounds[0].items:
            messagebox.showinfo("ไม่มีข้อมูล", "ไม่พบประวัติโจทย์ที่สามารถ Export ได้")
            return False

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="บันทึกประวัติเป็น PDF",
        )

        if not file_path:
            return False

        try:
            pdf_builder = PdfBuilder()
            build_field(self._rounds, pdf_builder)
            pdf_builder.generate(file_path)

            if source == "option":
                messagebox.showinfo("Export สำเร็จ", f"บันทึกไฟล์ PDF ได้ที่: {file_path}")
            return True

        except Exception as e:
            messagebox.showerror("Export ล้มเหลว", f"ไม่สามารถบันทึกไฟล์ PDF ได้: {e}")
            return False


if __name__ == "__main__":
    app = App()
    app.mainloop()
