from typing import Literal

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

        self.data = parent.getData()

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

        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        self.round_page = RoundPage(right_frame)
        self.round_page.grid(row=0, column=0, sticky="nsew")
        self.logo_page = LogoPage(right_frame, app=self.data)
        self.logo_page.grid(row=0, column=0, sticky="nsew")
        self.history_page = HistoryPage(right_frame, app=self.data)
        self.history_page.grid(row=0, column=0, sticky="nsew")

        self.round_page.tkraise()

        ttk.Label(
            left_frame,
            text="ตั้งค่า",
            font=("Arial", 16, "bold"),
            anchor="center",
            padding=(0, 5, 0, 0),
            style="light.Inverse.TLabel",
        ).pack(fill="x")

        ttk.Separator(left_frame).pack(fill="x", pady=10)

        self.round_page_btn = ttk.Button(
            left_frame,
            text="รอบและโจทย์",
            command=lambda: self.show_page("round"),
        )
        self.round_page_btn.pack(fill="x")

        self.logo_page_btn = ttk.Button(
            left_frame,
            text="ข้อมูลงานแข่งขัน",
            style="Outline.TButton",
            command=lambda: self.show_page("logo"),
        )
        self.logo_page_btn.pack(fill="x", pady=10)

        self.history_page_btn = ttk.Button(
            left_frame,
            text="ประวัติโจทย์",
            style="Outline.TButton",
            command=lambda: self.show_page("history"),
        )
        self.history_page_btn.pack(fill="x")

        a = ttk.Button(
            left_frame, text="ปิด", style="Link.TButton", command=self.destroy
        )
        a.pack(fill="x", expand=True, anchor="s")

    def show_page(self, page: Literal["round", "logo", "history"]):
        self.round_page_btn.configure(style="Outline.TButton")
        self.logo_page_btn.configure(style="Outline.TButton")
        self.history_page_btn.configure(style="Outline.TButton")

        if page == "round":
            self.round_page.tkraise()
            self.round_page_btn.configure(style="TButton")
        elif page == "logo":
            self.logo_page.tkraise()
            self.logo_page_btn.configure(style="TButton")
        elif page == "history":
            self.history_page.tkraise()
            self.history_page_btn.configure(style="TButton")
