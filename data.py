import ttkbootstrap as ttk


class AppData:
    def __init__(self, master):
        self.festname = ttk.StringVar(master, "คณิตศาสตร์วิชาการ")
        self.history = ttk.StringVar(master, "ประวัติโจทย์\n")
