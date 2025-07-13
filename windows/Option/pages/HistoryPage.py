from tkinter import messagebox

import ttkbootstrap as ttk

from interface import AppInterface


class HistoryPage(ttk.Frame):
    def __init__(self, master, app: AppInterface, **kwargs):
        super().__init__(master, padding=10, style="light.TFrame", **kwargs)

        self.app = app

        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=(0, 5))

        ttk.Label(
            top_frame,
            text="ประวัติโจทย์",
            style="light.Inverse.TLabel",
        ).pack(side="left", fill="both", expand=True)

        ttk.Button(
            top_frame,
            text="คัดลอก",
            style="TButton",
            command=self._copy_text,
        ).pack(side="right", fill="both")

        self.history_textbox = ttk.Text(self, state="disabled", wrap="word")
        self.history_textbox.configure(
            bg="#f9ffff", highlightbackground="#163557", highlightcolor="#163557"
        )
        self.history_textbox.pack(fill="both", expand=True)

        def update_history(*args):
            if str := app.history.get():
                try:
                    self.set_text(str)
                except ValueError:
                    pass

        app.history.trace_add("write", update_history)

        self.set_text(app.history.get())

    def set_text(self, text: str):
        self.history_textbox["state"] ="normal"
        self.history_textbox.delete(1.0, "end")
        self.history_textbox.insert("end", text)
        self.history_textbox["state"] ="disabled"

    def _copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self.app.history.get())
        messagebox.showinfo("คัดลอกสำเร็จ", "คัดลอกประวัติโจทย์เรียบร้อยแล้ว")
