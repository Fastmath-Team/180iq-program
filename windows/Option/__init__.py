from typing import Any, Literal, Optional

import ttkbootstrap as ttk

from interface import AppInterface
from windows.Option.pages.HistoryPage import HistoryPage
from windows.Option.pages.LogoPage import LogoPage
from windows.Option.pages.RoundPage import RoundPage

# import ttkbootstrap.constants as tc
# import ttkbootstrap.validation as tv


class OptionWindow(ttk.Toplevel):
    def __init__(self, parent: AppInterface):
        super().__init__(master=parent)

        self.app = parent

        self.title("ตั้งค่าการแข่งขัน — NSRU x Fastmath")
        self.geometry("640x480")
        self.minsize(640, 480)
        self.place_window_center()

        self._create_widgets()

    def _create_widgets(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        left_frame = ttk.Frame(self, padding=10, style="light.TFrame")
        left_frame.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        right_frame = ttk.Frame(self, style="light.TFrame")
        right_frame.grid(row=0, column=1, pady=10, padx=(0, 10), sticky="nsew")

        round_page = RoundPage(right_frame)
        logo_page = LogoPage(right_frame, app=self.app)
        history_page = HistoryPage(right_frame, app=self.app)

        ttk.Label(
            left_frame,
            text="ตั้งค่า",
            font=("Arial", 16, "bold"),
            anchor="center",
            padding=(0, 5, 0, 0),
            style="light.Inverse.TLabel",
        ).pack(fill="x")

        ttk.Separator(left_frame).pack(fill="x", pady=10)

        round_page_btn = ttk.Button(
            left_frame,
            text="รอบและโจทย์",
            style="secondary.TButton",
            command=lambda: self._show_page("round"),
        )
        round_page_btn.pack(fill="x")

        logo_page_btn = ttk.Button(
            left_frame,
            text="ข้อมูลงานแข่งขัน",
            style="secondary.TButton",
            command=lambda: self._show_page("logo"),
        )
        logo_page_btn.pack(fill="x", pady=10)

        history_page_btn = ttk.Button(
            left_frame,
            text="ประวัติโจทย์",
            style="secondary.TButton",
            command=lambda: self._show_page("history"),
        )
        history_page_btn.pack(fill="x")

        ttk.Button(
            left_frame, text="ปิด", style="Link.TButton", command=self.destroy
        ).pack(fill="x", expand=True, anchor="s")

        self._current_page: Optional[str] = None
        self._pages: dict[str, tuple[ttk.Button, ttk.Frame]] = {
            "round": (round_page_btn, round_page),
            "logo": (logo_page_btn, logo_page),
            "history": (history_page_btn, history_page),
        }

        self._show_page("round")


    def _show_page(self, page: str):
        if self._current_page:
            frame_btn, frame = self._pages[self._current_page]

            frame.pack_forget()
            frame_btn.configure(style="secondary.TButton")

        frame_btn, frame = self._pages[page]

        frame.pack(fill="both", expand=True)
        frame_btn.configure(style="TButton")

        self._current_page = page
