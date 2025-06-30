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

        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(
            self,
            text="คิดเลขเร็วคณิตศาสตร์วิชาการ",
            font=("Arial", 24, "bold"),
            justify=tc.CENTER,
        ).pack()

        cnt = Countdown(self, 5)
        cnt.pack()

        countdown_seconds = ttk.StringVar(value="30")

        spin = ttk.Spinbox(self, textvariable=countdown_seconds, from_=1, to=60)
        spin.pack()
        tv.add_validation(spin, validate_positive_number, "key")

        def handle_spin(*args):
            if x := countdown_seconds.get():
                try:
                    cnt.set_time(int(x))
                except ValueError:
                    pass

        countdown_seconds.trace_add("write", handle_spin)


if __name__ == "__main__":
    app = App()
    app.mainloop()
