import ttkbootstrap as ttk
import ttkbootstrap.constants as tc
import ttkbootstrap.validation as tv

from components.Countdown import Countdown
from utils.validation import validate_positive_number


class App(ttk.Window):
    def __init__(self):
        super().__init__(themename="yeti")

        self.title("คิดเลขเร็วคณิตศาสตร์วิชาการ — NSRU x Fastmath")
        self.geometry("800x600")
        self.minsize(800, 600)
        self.place_window_center()

        self._create_widgets()

    def _create_widgets(self):
        self.style.configure("TButton", font=(None, 16))

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

        ttk.Label(event_title_area, text="โซนแสดงโลโก้", font=("Arial", 16)).pack(
            side="left", fill="both", expand=True
        )

        ttk.Label(
            event_title_area,
            text="คณิตศาสตร์วิชาการ",
            font=("Arial", 16),
            anchor="e",
        ).pack(side="right", fill="both", expand=True)

        problem_frame = ttk.Frame(left_frame, padding=10, bootstyle="light")
        problem_frame.pack(fill="both", padx=(10, 0), pady=(10, 5), expand=True)

        problem_frame.rowconfigure(0, weight=1)
        problem_frame.columnconfigure(0, weight=1)

        problem_center_frame = ttk.Frame(problem_frame, bootstyle="light")
        problem_center_frame.grid(row=0, column=0)

        for i in range(5):
            ttk.Label(
                problem_center_frame,
                text="0",
                font=("Arial", 96, "bold"),
                anchor="center",
                bootstyle="inverse-light",
            ).grid(row=0, padx=5, column=i)

        answer_frame = ttk.Frame(left_frame, padding=10, bootstyle="light")
        answer_frame.pack(fill="both", padx=(10, 0), pady=(5, 10), expand=True)

        answer_frame.rowconfigure(0, weight=1)
        answer_frame.columnconfigure(0, weight=1)

        answer_center_frame = ttk.Frame(answer_frame, bootstyle="light")
        answer_center_frame.grid(row=0, column=0)

        for i in range(3):
            ttk.Label(
                answer_center_frame,
                text="0",
                font=("Arial", 96, "bold"),
                anchor="center",
                bootstyle="inverse-light",
            ).grid(row=0, padx=5, column=i)

        # --- RIGHT SIDE ---
        ttk.Label(right_frame, text="Powered by Fastmath.io", anchor="e").pack(
            fill="x", pady=(10, 0), padx=10
        )

        round_frame = ttk.Frame(right_frame, padding=10, bootstyle="light")
        round_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            round_frame,
            text="รอบที่ 1 ข้อที่ 1",
            font=("Arial", 16),
            anchor="center",
            bootstyle="inverse-light",
        ).pack(fill="x")

        cnt = Countdown(right_frame, 30)
        cnt.pack(fill="both", padx=10, expand=True)

        action_frame = ttk.Frame(right_frame, padding=10, bootstyle="light")
        action_frame.pack(fill="x", padx=10, pady=10)

        self.style.configure("Large.warning.TButton", font=(None, 24))
        self.style.configure("Large.success.TButton", font=(None, 24))

        get_question_btn = ttk.Button(
            action_frame, text="สุ่มโจทย์", padding=10, bootstyle="warning"
        )
        get_question_btn.configure(style="Large.warning.TButton")
        get_question_btn.pack(fill="x")

        get_answer_btn = ttk.Button(
            action_frame, text="สุ่มคำตอบ", padding=10, bootstyle="success"
        )
        get_answer_btn.configure(style="Large.success.TButton")
        get_answer_btn.pack(fill="x", pady=10)

        action_ext_frame = ttk.Frame(action_frame, bootstyle="light")
        action_ext_frame.pack(fill="x")

        action_ext_frame.columnconfigure(1, weight=1)

        self.style.configure("Small.Outline.TButton", font=(None, 12))

        prev_btn = ttk.Button(action_ext_frame, text="⬅︎", bootstyle="outline")
        prev_btn.configure(style="Small.Outline.TButton")
        prev_btn.grid(row=0, column=0, sticky="w")

        next_btn = ttk.Button(action_ext_frame, text="ข้อถัดไป", bootstyle="outline")
        next_btn.configure(style="Small.Outline.TButton")
        next_btn.grid(row=0, column=1, sticky="ew", padx=10)

        config_btn = ttk.Button(action_ext_frame, text="⚙️", bootstyle="outline")
        config_btn.configure(style="Small.Outline.TButton")
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


if __name__ == "__main__":
    app = App()
    app.mainloop()
