import math
from typing import Literal

import customtkinter as ctk
from PIL import Image


def update_logo_in_frame(
    filepaths: tuple[str, ...] | Literal[""],
    frame: ctk.CTkFrame | ctk.CTkScrollableFrame,
    reference: list[ctk.CTkImage],
    size=24,
    padx=(0, 10),
):
    if not filepaths:
        return

    for widget in frame.winfo_children():
        widget.destroy()
    reference.clear()

    for path in filepaths:
        try:
            img = Image.open(path)
            img_width, img_height = img.size
            photo = ctk.CTkImage(
                light_image=img, size=(math.ceil(img_width / img_height * size), size)
            )

            img_label = ctk.CTkLabel(frame, text="", image=photo)
            img_label.pack(side="left", padx=padx)

            reference.append(photo)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
