import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk

from interface import AppInterface
from utils.logo import update_logo_in_frame


class LogoPage(ctk.CTkFrame):
    def __init__(self, master, app: AppInterface, **kwargs):
        from styles import font as FONT

        super().__init__(master, **kwargs)

        self._app = app
        self._drag_start_x = 0
        self._dragged_widget = None

        ctk.CTkLabel(
            self, text="ระบุชื่องาน", font=FONT.StaticFont16Bold, anchor="w"
        ).pack(fill="x", padx=10, pady=(10, 5))

        festname = tk.StringVar(value=self._app.festname)

        def update_festname(*_):
            self._app.festname = festname.get()

        festname.trace_add("write", update_festname)

        ctk.CTkEntry(self, textvariable=festname, placeholder_text="ชื่องานแข่ง").pack(
            fill="x", padx=10
        )

        select_logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        select_logo_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            select_logo_frame, text="โลโก้งาน", font=FONT.StaticFont16Bold, anchor="w"
        ).pack(side="left", fill="both", expand=True)

        def select_images():
            filetypes = [("ไฟล์รูปภาพ", "*.png *.jpg *.jpeg *.gif *.bmp")]
            filepaths = filedialog.askopenfilenames(
                title="เลือกโลโก้", filetypes=filetypes
            )
            self._app.logo_filepaths += tuple(filepaths)
            self._update_logo_frame()
            self._app.update_logo(None)

        select_button = ctk.CTkButton(
            select_logo_frame, text="เลือกโลโก้", command=select_images, width=0
        )
        select_button.pack(side="right", fill="both")

        self.image_references: list[ctk.CTkImage] = []

        self.logo_frame = ctk.CTkScrollableFrame(
            self, orientation="horizontal", height=72
        )
        self.logo_frame.pack(fill="x", padx=10)

        self._update_logo_frame()

    def _delete_logo(self, path_to_delete: str):
        updated_filepaths = tuple(
            p for p in self._app.logo_filepaths if p != path_to_delete
        )
        self._app.logo_filepaths = updated_filepaths
        self._update_logo_frame()
        self._app.update_logo(None)

    def _start_drag(self, event, path):
        self._dragged_widget = event.widget
        self._dragged_widget.lift()
        self._drag_start_x = event.x
        self._original_path = path

    def _drag_motion(self, event):
        if self._dragged_widget:
            # คำนวณตำแหน่งใหม่โดยใช้พิกัดหน้าจอ
            x_new = self._dragged_widget.winfo_x() + event.x - self._drag_start_x
            self._dragged_widget.place(x=x_new, y=0)

    def _end_drag(self, event):
        if self._dragged_widget:
            # คำนวณตำแหน่งใหม่
            logo_widgets = self.logo_frame.winfo_children()
            new_index = 0
            for i, widget in enumerate(logo_widgets):
                if event.x_root > widget.winfo_rootx() + widget.winfo_width() / 2:
                    new_index = i + 1

            current_filepaths = list(self._app.logo_filepaths)

            if self._original_path in current_filepaths:
                old_index = current_filepaths.index(self._original_path)

                if new_index != old_index and new_index != old_index + 1:
                    item = current_filepaths.pop(old_index)
                    if new_index > old_index:
                        new_index -= 1
                    current_filepaths.insert(new_index, item)

                    self._app.logo_filepaths = tuple(current_filepaths)
                    self._update_logo_frame()
                    self._app.update_logo(None)

            self._dragged_widget = None

    def _update_logo_frame(self):
        update_logo_in_frame(
            self._app.logo_filepaths, self.logo_frame, self.image_references, 64
        )

        for widget in self.logo_frame.winfo_children():
            path = self._app.logo_filepaths[
                list(self.logo_frame.winfo_children()).index(widget)
            ]

            widget.bind("<Button-1>", lambda event, p=path: self._start_drag(event, p))
            widget.bind("<B1-Motion>", self._drag_motion)
            widget.bind("<ButtonRelease-1>", self._end_drag)

            widget.bind("<Button-3>", lambda event, p=path: self._delete_logo(p))
