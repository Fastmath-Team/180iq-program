import platform
import tkinter as tk
from typing import Optional

import customtkinter as ctk

from interface import AppInterface
from styles.buttons import BUTTON_DEFAULT_STYLES, BUTTON_FILLED_STYLES
from utils.file import get_file
from windows.Option.pages.HistoryPage import HistoryPage
from windows.Option.pages.LogoPage import LogoPage
from windows.Option.pages.RoundPage import RoundPage


class OptionWindow(ctk.CTkToplevel):
    def __init__(self, parent: AppInterface):
        super().__init__(master=parent)

        self.app = parent

        self.title("ตั้งค่าการแข่งขัน — MathStat NSRU X Fastmath")
        self.geometry("640x480")
        self.minsize(640, 480)

        if platform.system() == "Windows":
            self.iconbitmap(get_file("assets/acad10.ico"))

        self._icon_photo_image = tk.PhotoImage(file=get_file("assets/acad10.png"))
        self.iconphoto(True, self._icon_photo_image)

        self._page_instances: dict[str, ctk.CTkFrame] = {}

        self._create_widgets()

    def _create_widgets(self):
        from styles import font as FONT

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(self)
        left_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        self.right_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.right_frame.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="nsew")

        ctk.CTkLabel(left_frame, text="ตั้งค่า", font=FONT.StaticFont16Bold).pack(
            fill="x", pady=10
        )

        round_page_btn = ctk.CTkButton(
            left_frame,
            text="รอบการแข่งขัน",
            command=lambda: self._show_page("round"),
            **BUTTON_FILLED_STYLES,
        )
        round_page_btn.pack(fill="x", padx=10)

        logo_page_btn = ctk.CTkButton(
            left_frame, text="ข้อมูลงานแข่งขัน", command=lambda: self._show_page("logo")
        )
        logo_page_btn.pack(fill="x", pady=10, padx=10)

        history_page_btn = ctk.CTkButton(
            left_frame, text="ประวัติโจทย์", command=lambda: self._show_page("history")
        )
        history_page_btn.pack(fill="x", padx=10)

        ctk.CTkFrame(left_frame, fg_color="transparent").pack(expand=True, fill="both")

        save_btn = ctk.CTkButton(
            left_frame, text="บันทึก", command=self._on_save_and_close
        )
        save_btn.pack(fill="x", padx=10, pady=(0, 5))

        reset_btn = ctk.CTkButton(
            left_frame, text="เคลียร์การตั้งค่า", command=self._on_reset_settings
        )
        reset_btn.pack(fill="x", padx=10, pady=(0, 5))

        ctk.CTkLabel(left_frame, text=f"เวอร์ชัน {self.app.version}").pack(
            fill="x", anchor="s", padx=10
        )

        self._current_page: Optional[str] = None
        self._pages: dict[str, tuple[ctk.CTkButton, type[ctk.CTkFrame]]] = {
            "round": (round_page_btn, RoundPage),
            "logo": (logo_page_btn, LogoPage),
            "history": (history_page_btn, HistoryPage),
        }

        self._page_instances["round"] = RoundPage(self.right_frame, app=self.app)
        self._show_page("round")

    def _show_page(self, page: str):
        if self._current_page:
            frame_btn, _ = self._pages[self._current_page]
            frame_instance = self._page_instances[self._current_page]

            frame_instance.pack_forget()
            frame_btn.configure(**BUTTON_DEFAULT_STYLES)

        frame_btn, page_class = self._pages[page]

        if page not in self._page_instances:
            self._page_instances[page] = page_class(self.right_frame, app=self.app)

        frame_instance = self._page_instances[page]
        frame_instance.pack(fill="both", expand=True)
        frame_btn.configure(**BUTTON_FILLED_STYLES)

        self._current_page = page

    def _on_save_and_close(self):
        self.app.save_settings()
        self.destroy()

    def _on_reset_settings(self):
        self.app.reset_settings()
        self.destroy()
