from typing import Callable
from interface import Round

import ttkbootstrap as ttk

class RoundOptionFrame(ttk.Frame):
    def __init__(
        self,
        master,

        index: int,
        round: Round,

        on_remove: Callable[[int], None],

        **kwargs
    ):
        super().__init__(master, padding=1, **kwargs)

        self._items = round.items

        option = round.options

        # added to self to prevent GC
        # https://stackoverflow.com/a/37351021/2736814
        self._question_count = question_count = ttk.IntVar(value=option.question_count)
        self._time_per_question = time_per_question = ttk.IntVar(value=option.time_per_question)
        self._question_digit = question_digit = ttk.IntVar(value=option.question_digit)
        self._answer_digit = answer_digit = ttk.IntVar(value=option.answer_digit)

        master_frame = ttk.Frame(
            self, padding=10, style="lighter.light.TFrame"
        )
        master_frame.pack(fill="both", expand=True)

        title_frame = ttk.Frame(master_frame)
        title_frame.pack(fill="x")

        self._round_label = round_label = ttk.Label(
            title_frame,
            style="light.Inverse.TLabel",
        )
        round_label.pack(side="left", fill="both", expand=True)

        self._remove_btn = ttk.Button(
            title_frame,
            text="ลบรอบ",
            style="TButton",
            command=lambda: on_remove(self._index),
        )

        options_grid = ttk.Frame(master_frame)
        options_grid.pack(fill="x", pady=5, expand=True)

        options_grid.columnconfigure(0, weight=0)
        options_grid.columnconfigure(1, weight=1)
        options_grid.columnconfigure(2, weight=0)
        options_grid.columnconfigure(3, weight=1)

        ttk.Label(options_grid, text="จำนวนข้อ").grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Spinbox(
            options_grid,
            from_=1,
            to=100,
            textvariable=question_count,
        ).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(options_grid, text="ระยะเวลา (วินาที)").grid(
            row=0, column=2, sticky="e", padx=5, pady=5
        )
        ttk.Spinbox(
            options_grid,
            from_=10,
            to=60,
            textvariable=time_per_question,
        ).grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(options_grid, text="จำนวนเลขสุ่มในโจทย์").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Combobox(
            options_grid,
            state="readonly",
            values=["3", "4", "5"],
            textvariable=question_digit,
        ).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(options_grid, text="จำนวนหลักของคำตอบ").grid(
            row=1, column=2, sticky="e", padx=5, pady=5
        )
        ttk.Combobox(
            options_grid,
            state="readonly",
            values=["1", "2", "3"],
            textvariable=answer_digit,
        ).grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(
            master_frame,
            text="ตำแหน่งของเลขสุ่มที่ต้องการเน้นสี",
            style="light.Inverse.TLabel",
        ).pack(fill="both")

        highlight_frame = ttk.Frame(
            master_frame, style="lighter.light.TFrame"
        )
        highlight_frame.pack(fill="x", pady=(10, 0))

        current_digits: list[ttk.Checkbutton] = []

        # capture loop variables
        def on_update_highlighted_digits(i: int, check_var: ttk.BooleanVar):
            return lambda *_: (
                option.highlighted_question_digits.add(i) if check_var.get() else
                option.highlighted_question_digits.discard(i)
            )

        def redraw_checkboxes():
            for i, check in enumerate(current_digits):
                check.destroy()

                highlight_frame.columnconfigure(i, weight=0)

            current_digits.clear()

            for i in range(option.question_digit):
                check_var = ttk.BooleanVar(value=i in option.highlighted_question_digits)
                check_var.trace_add("write", on_update_highlighted_digits(i, check_var))

                highlight_frame.columnconfigure(i, weight=1)

                check = ttk.Checkbutton(
                    highlight_frame,
                    text=f"{i + 1}",
                    variable=check_var,
                )
                check.grid(row=0, column=i)


                current_digits.append(check)

        redraw_checkboxes()

        def on_question_count_changed(*_): option.question_count = question_count.get()
        def on_time_per_question_changed(*_): option.time_per_question = time_per_question.get()
        def on_question_digit_changed(*_):
            option.question_digit = question_digit.get()

            redraw_checkboxes()

        def on_answer_digit_changed(*_): option.answer_digit = answer_digit.get()

        question_count.trace_add("write", on_question_count_changed)
        time_per_question.trace_add("write", on_time_per_question_changed)
        question_digit.trace_add("write", on_question_digit_changed)
        answer_digit.trace_add("write", on_answer_digit_changed)

        self.set_index(index, False)

    def set_index(self, index: int, can_delete: bool):
        self._index = index

        self._round_label["text"] = f"รอบที่ {index + 1}"

        if can_delete and len(self._items) == 0:
            self._remove_btn.pack(side="right", fill="both")
        else:
            self._remove_btn.pack_forget()
