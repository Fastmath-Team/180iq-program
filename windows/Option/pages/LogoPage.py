import ttkbootstrap as ttk

from data import AppData


class LogoPage(ttk.Frame):
    def __init__(self, master, app: AppData, **kwargs):
        super().__init__(master, padding=10, style="light.TFrame", **kwargs)

        ttk.Label(
            self,
            text="ระบุชื่องาน",
            style="light.Inverse.TLabel",
        ).pack(fill="x", pady=(0, 5))

        ttk.Entry(self, textvariable=app.festname, style="dark.TEntry").pack(fill="x")
