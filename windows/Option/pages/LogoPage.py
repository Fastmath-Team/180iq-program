from tkinter import filedialog

import customtkinter as ctk
from PIL import ImageTk

from interface import AppInterface
from utils.logo import update_logo_in_frame


class LogoPage(ctk.CTkFrame):
    def __init__(self, master, app: AppInterface, **kwargs):
        super().__init__(master, **kwargs)

        ctk.CTkLabel(self, text="ระบุชื่องาน", anchor="w").pack(
            fill="x", padx=10, pady=(10, 5)
        )

        ctk.CTkEntry(self, textvariable=app.festname, placeholder_text="ชื่องานแข่ง").pack(
            fill="x", padx=10
        )

        select_logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        select_logo_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(select_logo_frame, text="โลโก้งาน", anchor="w").pack(
            side="left", fill="both", expand=True
        )

        def select_images():
            filetypes = [("ไฟล์รูปภาพ", "*.png *.jpg *.jpeg *.gif *.bmp")]
            filepaths = filedialog.askopenfilenames(
                title="เลือกโลโก้", filetypes=filetypes
            )

            update_logo_in_frame(filepaths, self.logo_frame, self.image_references, 64)
            app.update_logo(filepaths)

        select_button = ctk.CTkButton(
            select_logo_frame,
            text="เลือกโลโก้",
            command=select_images,
        )
        select_button.pack(side="right", fill="both")

        self.image_references: list[ImageTk.PhotoImage] = []

        self.logo_frame = ctk.CTkScrollableFrame(
            self, orientation="horizontal", height=72
        )
        self.logo_frame.pack(fill="x", padx=10)
