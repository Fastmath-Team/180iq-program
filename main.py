import ttkbootstrap as ttk
import ttkbootstrap.constants as tc


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
        ).pack(expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
