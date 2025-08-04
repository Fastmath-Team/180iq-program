import math
from typing import Callable, Literal

import customtkinter as ctk
from PIL import Image


def update_logo_in_frame(
    filepaths: tuple[str, ...] | Literal[""],
    frame: ctk.CTkFrame | ctk.CTkScrollableFrame,
    reference: list[ctk.CTkImage],
    size: int = 24,
    padx=(0, 10),
    on_click: Callable[[str], None] | None = None,
):
    for widget in frame.winfo_children():
        widget.destroy()

    reference.clear()

    # ที่ล้างก่อนเพราะว่าเผื่อไม่เอาโลโก้เลย
    if not filepaths:
        return

    for path in filepaths:
        try:
            img = Image.open(path)
            img_width, img_height = img.size
            photo = ctk.CTkImage(
                light_image=img, size=(math.ceil(img_width / img_height * size), size)
            )

            img_label = ctk.CTkLabel(frame, text="", image=photo, cursor="hand2")
            img_label.pack(side="left", padx=padx)

            reference.append(photo)

            if on_click:
                img_label.bind("<Button-1>", lambda _, p=path: on_click(p))

        except Exception as e:
            print(f"Error loading image {path}: {e}")
