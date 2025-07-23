import tkinter as tk
from tkinter import filedialog

import customtkinter as ctk

from interface import AppInterface
from utils.logo import update_logo_in_frame


class LogoPage(ctk.CTkFrame):
    def __init__(self, master, app: AppInterface, **kwargs):
        from styles import font as FONT

        super().__init__(master, **kwargs)

        ctk.CTkLabel(self, text="ระบุชื่องาน", font=FONT.Font16Bold, anchor="w").pack(
            fill="x", padx=10, pady=(10, 5)
        )

        festname = tk.StringVar(value=app.festname)

        def update_festname(*_):
            app.festname = festname.get()

        festname.trace_add("write", update_festname)

        ctk.CTkEntry(self, textvariable=festname, placeholder_text="ชื่องานแข่ง").pack(
            fill="x", padx=10
        )

        select_logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        select_logo_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            select_logo_frame, text="โลโก้งาน", font=FONT.Font16Bold, anchor="w"
        ).pack(side="left", fill="both", expand=True)

        def select_images():
            filetypes = [("ไฟล์รูปภาพ", "*.png *.jpg *.jpeg *.gif *.bmp")]
            filepaths = filedialog.askopenfilenames(
                title="เลือกโลโก้", filetypes=filetypes
            )

            update_logo_in_frame(filepaths, self.logo_frame, self.image_references, 64)
            app.update_logo(filepaths)

        select_button = ctk.CTkButton(
            select_logo_frame, text="เลือกโลโก้", command=select_images, width=0
        )
        select_button.pack(side="right", fill="both")

        self.image_references: list[ctk.CTkImage] = []

        self.logo_frame = ctk.CTkScrollableFrame(
            self, orientation="horizontal", height=72
        )
        self.logo_frame.pack(fill="x", padx=10)
