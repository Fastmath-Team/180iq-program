import ttkbootstrap as ttk


class RoundPage(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=10, style="light.TFrame", **kwargs)

        ttk.Label(
            self,
            text="RoundPage",
            style="light.Inverse.TLabel",
        ).pack(fill="x", pady=(0, 5))
