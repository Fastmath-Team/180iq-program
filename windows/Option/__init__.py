from typing import Optional

import customtkinter as ctk

from interface import AppInterface
from styles.buttons import BUTTON_DEFAULT_STYLES, BUTTON_FILLED_STYLES
from windows.Option.pages.HistoryPage import HistoryPage
from windows.Option.pages.LogoPage import LogoPage
from windows.Option.pages.RoundPage import RoundPage


class OptionWindow(ctk.CTkToplevel):
    def __init__(self, parent: AppInterface):
        super().__init__(master=parent)

        self.app = parent

        self.title("ตั้งค่าการแข่งขัน — Fastmath")
        self.geometry("640x480")
        self.minsize(640, 480)

        self._create_widgets()

    def _create_widgets(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left_frame = ctk.CTkFrame(self)
        left_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        right_frame = ctk.CTkFrame(self, fg_color="transparent")
        right_frame.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="nsew")

        round_page = RoundPage(right_frame, app=self.app)
        logo_page = LogoPage(right_frame, app=self.app)
        history_page = HistoryPage(right_frame, app=self.app)

        ctk.CTkLabel(left_frame, text="ตั้งค่า", font=("Arial", 16, "bold")).pack(
            fill="x", pady=10
        )

        round_page_btn = ctk.CTkButton(
            left_frame,
            text="รอบและโจทย์",
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

        ctk.CTkButton(left_frame, text="ปิด", command=self.destroy).pack(
            fill="x", expand=True, anchor="s", padx=10, pady=10
        )

        self._current_page: Optional[str] = None
        self._pages: dict[str, tuple[ctk.CTkButton, ctk.CTkFrame]] = {
            "round": (round_page_btn, round_page),
            "logo": (logo_page_btn, logo_page),
            "history": (history_page_btn, history_page),
        }

        self._show_page("round")

    def _show_page(self, page: str):
        if self._current_page:
            frame_btn, frame = self._pages[self._current_page]

            frame.pack_forget()
            frame_btn.configure(**BUTTON_DEFAULT_STYLES)

        frame_btn, frame = self._pages[page]

        frame.pack(fill="both", expand=True)
        frame_btn.configure(**BUTTON_FILLED_STYLES)

        self._current_page = page
