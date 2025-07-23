import tkinter as tk
from typing import Callable

import customtkinter as ctk

from interface import AppInterface, Round
from styles.theme import THEME


class RoundOptionFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        index: int,
        round: Round,
        app: AppInterface,
        on_remove: Callable[[int], None],
        **kwargs,
    ):
        super().__init__(master, fg_color=THEME.CTkFrame.fg_color[0], **kwargs)

        self._app = app
        self._items = round.items

        option = round.options

        # added to self to prevent GC
        # https://stackoverflow.com/a/37351021/2736814
        self._question_count = question_count = tk.IntVar(value=option.question_count)
        self._time_per_question = time_per_question = tk.IntVar(
            value=option.time_per_question
        )
        self._question_digit = question_digit = tk.IntVar(value=option.question_digit)
        self._answer_digit = answer_digit = tk.IntVar(value=option.answer_digit)

        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=10, pady=(10, 0))

        self._round_label = round_label = ctk.CTkLabel(
            title_frame, text="", font=(None, 12, "bold"), anchor="w"
        )
        round_label.pack(side="left", fill="both", expand=True)

        self._remove_btn = ctk.CTkButton(
            title_frame, text="ลบรอบ", command=lambda: on_remove(self._index), width=0
        )

        options_grid = ctk.CTkFrame(self, fg_color="transparent")
        options_grid.pack(fill="x", padx=5, pady=(5, 0), expand=True)

        options_grid.columnconfigure(0, weight=0)
        options_grid.columnconfigure(1, weight=1)
        options_grid.columnconfigure(2, weight=0)
        options_grid.columnconfigure(3, weight=1)

        ctk.CTkLabel(options_grid, text="จำนวนข้อ").grid(
            row=0, column=0, sticky="e", padx=(5, 0), pady=5
        )
        self._question_count_entry = question_count_entry = ctk.CTkEntry(
            options_grid, textvariable=question_count
        )
        question_count_entry.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=5)

        ctk.CTkLabel(options_grid, text="ระยะเวลา (วินาที)").grid(
            row=0, column=2, sticky="e", padx=(5, 0), pady=5
        )
        time_per_question_entry = ctk.CTkEntry(
            options_grid, textvariable=time_per_question
        )
        time_per_question_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(options_grid, text="จำนวนเลขสุ่มในโจทย์").grid(
            row=1, column=0, sticky="e", padx=(5, 0), pady=5
        )
        ctk.CTkComboBox(
            options_grid,
            state="readonly",
            values=["3", "4", "5"],
            variable=question_digit,
        ).grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=5)

        ctk.CTkLabel(options_grid, text="จำนวนหลักของคำตอบ").grid(
            row=1, column=2, sticky="e", padx=(5, 0), pady=5
        )
        ctk.CTkComboBox(
            options_grid,
            state="readonly",
            values=["1", "2", "3"],
            variable=answer_digit,
        ).grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        ctk.CTkLabel(self, text="ตำแหน่งของเลขสุ่มที่ต้องการเน้นสี", anchor="w").pack(
            fill="both", padx=10
        )

        highlight_frame = ctk.CTkFrame(self, fg_color="transparent")
        highlight_frame.pack(fill="x", padx=10, pady=(5, 10))

        current_digits: list[ctk.CTkCheckBox] = []

        # capture loop variables
        def on_update_highlighted_digits(i: int, check_var: tk.BooleanVar):
            def on(*_):
                if check_var.get():
                    option.highlighted_question_digits.add(i)
                else:
                    option.highlighted_question_digits.discard(i)

                app.trigger_update_rounds("highlighted_question_digits")

            return on

        def redraw_checkboxes():
            for i, check in enumerate(current_digits):
                check.destroy()

                highlight_frame.columnconfigure(i, weight=0)

            current_digits.clear()

            for i in range(option.question_digit):
                check_var = tk.BooleanVar(value=i in option.highlighted_question_digits)
                check_var.trace_add("write", on_update_highlighted_digits(i, check_var))

                highlight_frame.columnconfigure(i, weight=1)

                check = ctk.CTkCheckBox(
                    highlight_frame,
                    text=f"{i + 1}",
                    variable=check_var,
                )
                check.grid(row=0, column=i)

                current_digits.append(check)

        redraw_checkboxes()

        def on_question_count_changed(*_):
            try:
                count = question_count.get()
                assert 0 < count < 100
            except (tk.TclError, AssertionError):
                question_count_entry.configure(border_color="red", border_width=2)
                return

            question_count_entry.configure(
                border_color=THEME.CTkEntry.border_color[0],
                border_width=THEME.CTkEntry.border_width,
            )
            option.question_count = count

        def on_time_per_question_changed(*_):
            try:
                seconds = time_per_question.get()
                assert 0 < seconds < 100
            except (tk.TclError, AssertionError):
                time_per_question_entry.configure(border_color="red", border_width=2)
                return

            time_per_question_entry.configure(
                border_color=THEME.CTkEntry.border_color[0],
                border_width=THEME.CTkEntry.border_width,
            )
            option.time_per_question = seconds

            app.trigger_update_rounds("timer")

        def on_question_digit_changed(*_):
            option.question_digit = question_digit.get()

            redraw_checkboxes()

            app.trigger_update_rounds("question_digit")

        def on_answer_digit_changed(*_):
            option.answer_digit = answer_digit.get()

            app.trigger_update_rounds("answer_digit")

        question_count.trace_add("write", on_question_count_changed)
        time_per_question.trace_add("write", on_time_per_question_changed)
        question_digit.trace_add("write", on_question_digit_changed)
        answer_digit.trace_add("write", on_answer_digit_changed)

        self.set_index(index)

    def set_index(self, index: int):
        can_delete = len(self._app.rounds) > 1 and len(self._items) == 0

        self._index = index

        self._round_label.configure(text=f"รอบที่ {index + 1}")
        self._question_count_entry.configure(
            state="normal" if can_delete else "disabled"
        )

        if can_delete:
            self._remove_btn.pack(side="right", fill="both")
        else:
            self._remove_btn.pack_forget()
