import ttkbootstrap as ttk

class AppInterface:
    @property
    def festname(self) -> ttk.StringVar:
        raise NotImplementedError()

    @property
    def history(self) -> ttk.StringVar:
        raise NotImplementedError()
