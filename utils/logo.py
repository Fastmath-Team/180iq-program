from typing import Literal

import customtkinter as ctk
from PIL import Image


def update_logo_in_frame(
    filepaths: tuple[str, ...] | Literal[""],
    frame: ctk.CTkFrame,
    reference: list[ctk.CTkImage],
    size=24,
):
    if not filepaths:
        return

    for widget in frame.winfo_children():
        widget.destroy()
    reference.clear()

    for path in filepaths:
        try:
            img = Image.open(path)
            img.thumbnail((size, size), Image.Resampling.LANCZOS)
            photo = ctk.CTkImage(light_image=img, size=(size, size))

            img_label = ctk.CTkLabel(frame, text="", image=photo)
            img_label.pack(side="left", padx=(0, 10))

            reference.append(photo)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
