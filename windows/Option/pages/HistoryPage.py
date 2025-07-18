from tkinter import messagebox

import customtkinter as ctk

from interface import AppInterface


class HistoryPage(ctk.CTkFrame):
    def __init__(self, master, app: AppInterface, **kwargs):
        super().__init__(master, **kwargs)

        self._app = app

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(top_frame, text="ประวัติโจทย์", anchor="w").pack(
            side="left", fill="both", expand=True
        )

        ctk.CTkButton(
            top_frame,
            text="คัดลอก",
            command=self._copy_text,
        ).pack(side="right", fill="both")

        self._history_textbox = ctk.CTkTextbox(self, state="disabled", wrap="word")
        self._history_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        def update_history(*args):
            if str := app.history.get():
                try:
                    self._set_text(str)
                except ValueError:
                    pass

        app.history.trace_add("write", update_history)

        self._set_text(app.history.get())

    def _set_text(self, text: str):
        self._history_textbox.configure(state="normal")
        self._history_textbox.delete(1.0, "end")
        self._history_textbox.insert("end", text)
        self._history_textbox.configure(state="disabled")

    def _copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self._app.history.get())
        messagebox.showinfo("คัดลอกสำเร็จ", "คัดลอกประวัติโจทย์เรียบร้อยแล้ว")
