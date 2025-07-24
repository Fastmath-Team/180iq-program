import customtkinter as ctk

from utils.responsive import get_responsive_value_from_width

StaticFont13Bold = ctk.CTkFont(size=13, weight="bold")
StaticFont16Bold = ctk.CTkFont(size=16, weight="bold")

Font13 = ctk.CTkFont(size=13)
Font13Bold = ctk.CTkFont(size=13, weight="bold")
Font16 = ctk.CTkFont(size=16)
Font16Bold = ctk.CTkFont(size=16, weight="bold")
Font24 = ctk.CTkFont(size=24)
Font80Bold = ctk.CTkFont(size=80, weight="bold")
Font108Bold = ctk.CTkFont(size=108, weight="bold")

RESPONSIVE_FONT_DATA = [
    (Font13, (13, 16, 24, 32)),
    (Font13Bold, (13, 16, 24, 32)),
    (Font16, (16, 22, 28, 38)),
    (Font16Bold, (16, 22, 28, 38)),
    (Font24, (24, 32, 42, 56)),
    (Font80Bold, (80, 107, 142, 189)),
    (Font108Bold, (108, 144, 192, 256)),
]


def update_font_size(width: int):
    width_index = get_responsive_value_from_width(width, (0, 1, 2, 3))

    for font, sizes in RESPONSIVE_FONT_DATA:
        font.configure(size=sizes[width_index])
