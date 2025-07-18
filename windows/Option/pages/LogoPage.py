from tkinter import filedialog

import customtkinter
import ttkbootstrap as ttk
from PIL import ImageTk

# from components.ScrolledFrame import ScrolledFrame
from interface import AppInterface
from utils.logo import update_logo_in_frame


class LogoPage(ttk.Frame):
    def __init__(self, master, app: AppInterface, **kwargs):
        super().__init__(master, padding=10, style="light.TFrame", **kwargs)

        ttk.Label(
            self,
            text="ระบุชื่องาน",
            style="light.Inverse.TLabel",
        ).pack(fill="x", pady=(0, 5))

        ttk.Entry(self, textvariable=app.festname, style="dark.TEntry").pack(fill="x")

        select_logo_frame = ttk.Frame(self)
        select_logo_frame.pack(fill="x", pady=10)

        ttk.Label(
            select_logo_frame,
            text="เลือกโลโก้",
            style="light.Inverse.TLabel",
        ).pack(side="left", fill="both", expand=True)

        def select_images():
            filetypes = [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
            filepaths = filedialog.askopenfilenames(
                title="Select Images", filetypes=filetypes
            )

            update_logo_in_frame(filepaths, self.logo_frame, self.image_references, 64)
            app.update_logo(filepaths)

        select_button = ttk.Button(
            select_logo_frame,
            text="Select Images",
            command=select_images,
        )
        select_button.pack(side="right", fill="both")

        self.image_references: list[ImageTk.PhotoImage] = []

        self.logo_frame = customtkinter.CTkScrollableFrame(
            self, orientation="horizontal", height=64
        )
        self.logo_frame.pack(fill="x")
