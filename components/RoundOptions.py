from typing import Callable, Self
import ttkbootstrap as ttk


class RoundOptions(ttk.Frame):
    def __init__(self, master, on_remove: Callable[[Self], None], **kwargs):
        super().__init__(master, padding=1, **kwargs)

        self.round = ttk.IntVar(value=1)

        self.question_count_var = ttk.StringVar(value="10")
        self.time_per_question = ttk.StringVar(value="30")
        self.question_digit = ttk.StringVar(value="4")
        self.question_answer_digit = ttk.StringVar(value="2")

        self.master_frame = master_frame = ttk.Frame(
            self, padding=10, style="lighter.light.TFrame"
        )
        master_frame.pack(fill="both", expand=True)

        title_frame = ttk.Frame(master_frame)
        title_frame.pack(fill="x")

        self.round_label = ttk.Label(
            title_frame,
            text=f"รอบที่ {self.round.get()}",
            style="light.Inverse.TLabel",
        )
        self.round_label.pack(side="left", fill="both", expand=True)

        def update_round_label(*args):
            self.round_label["text"] = f"รอบที่ {self.round.get()}"

        self.round.trace_add("write", update_round_label)

        ttk.Button(
            title_frame,
            text="ลบรอบ",
            style="TButton",
            command=lambda: on_remove(self),
        ).pack(side="right", fill="both")

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
            textvariable=self.question_count_var,
        ).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(options_grid, text="ระยะเวลา (วินาที)").grid(
            row=0, column=2, sticky="e", padx=5, pady=5
        )
        ttk.Spinbox(
            options_grid,
            from_=10,
            to=60,
            textvariable=self.time_per_question,
        ).grid(row=0, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(options_grid, text="จำนวนเลขสุ่มในโจทย์").grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )
        ttk.Combobox(
            options_grid,
            state="readonly",
            values=["3", "4", "5"],
            textvariable=self.question_digit,
        ).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(options_grid, text="จำนวนหลักของคำตอบ").grid(
            row=1, column=2, sticky="e", padx=5, pady=5
        )
        ttk.Combobox(
            options_grid,
            state="readonly",
            values=["1", "2", "3"],
            textvariable=self.question_answer_digit,
        ).grid(row=1, column=3, sticky="ew", padx=5, pady=5)

        ttk.Label(
            master_frame,
            text="ตำแหน่งของเลขสุ่มที่ต้องการเน้นสี",
            style="light.Inverse.TLabel",
        ).pack(fill="both")

        self.highlight_frame = None
        self.hightlighted_digits = [
            ttk.BooleanVar(),
            ttk.BooleanVar(),
            ttk.BooleanVar(),
            ttk.BooleanVar(),
            ttk.BooleanVar(),
        ]

        def handle_problem_digits(*args):
            if self.question_digit.get():
                try:
                    self._redisplay_checkboxes()
                except ValueError:
                    pass

        self.question_digit.trace_add("write", handle_problem_digits)

        self._redisplay_checkboxes()

    def _redisplay_checkboxes(self):
        if self.highlight_frame is not None:
            self.highlight_frame.destroy()

        self.highlight_frame = ttk.Frame(
            self.master_frame, style="lighter.light.TFrame"
        )
        self.highlight_frame.pack(fill="x", pady=(10, 0))

        for i in range(5):
            self.hightlighted_digits[i].set(False)

        for i in range(int(self.question_digit.get())):
            self.highlight_frame.columnconfigure(i, weight=1)
            check = ttk.Checkbutton(
                self.highlight_frame,
                text=f"{i + 1}",
                variable=self.hightlighted_digits[i],
            )
            check.grid(row=0, column=i)
