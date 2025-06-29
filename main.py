import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("คิดเลขเร็วคณิตศาสตร์วิชาการ")
        self.geometry("800x600")

        self._create_widgets()

    def _create_widgets(self):
        ttk.Label(
            self,
            text="คิดเลขเร็วคณิตศาสตร์วิชาการ",
            font=("Arial", 24, "bold"),
            justify=tk.CENTER,
        ).pack(expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()
