import ttkbootstrap as ttk


class Countdown(ttk.Frame):
    def __init__(self, master, defaulttime=30, **kwargs):
        super().__init__(master, style="light.TFrame", **kwargs)

        self.max_seconds = defaulttime
        self.remaining_seconds = defaulttime

        self.after_job_id = None

        self._create_widgets()

    def _create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.time_label = time_label = ttk.Label(
            self,
            font=("Arial", 96, "bold"),
            text=self.remaining_seconds,
            anchor="center",
            style="light.Inverse.TLabel",
        )
        time_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0), sticky="nsew")

        self.time_progress_bar = time_progress_bar = ttk.Progressbar(
            self,
            orient=ttk.VERTICAL,
            maximum=self.max_seconds,
            value=self.remaining_seconds,
        )
        time_progress_bar.grid(
            row=0, column=1, rowspan=2, padx=10, pady=10, sticky=ttk.NSEW
        )

        self.button = button = ttk.Button(
            self,
            text="จับเวลา",
            style="Medium.TButton",
            command=self._toggle_timer,
        )
        button.grid(row=1, column=0, padx=(10, 0), pady=10, sticky=ttk.NSEW)

    def _update_widgets(self):
        self.time_label["text"] = self.remaining_seconds
        self.time_progress_bar["value"] = self.remaining_seconds

    def set_time(self, time: int):
        self._cancel_job()

        self.max_seconds = time
        self.time_progress_bar["maximum"] = time

        self._reset_timer()

    def _toggle_timer(self):
        if self.remaining_seconds == self.max_seconds:
            self._start_timer()
        else:
            self._reset_timer()

    def _start_timer(self):
        self.button["text"] = "รีเซ็ต"

        self._update_widgets()
        self._schedule_job()

    def _reset_timer(self):
        self._cancel_job()

        self.button["text"] = "จับเวลา"

        self.remaining_seconds = self.max_seconds
        self._update_widgets()

    def _schedule_job(self):
        self.after_job_id = self.after(1000, self._tick)

    def _cancel_job(self):
        if self.after_job_id:
            self.after_cancel(self.after_job_id)
            self.after_job_id = None

    def _tick(self):
        self.remaining_seconds -= 1
        self._update_widgets()
        if self.remaining_seconds:
            self._schedule_job()
        else:
            # TODO - Play sound
            self._cancel_job()
