from typing import Literal

import ttkbootstrap as ttk
from PIL import Image, ImageTk


def update_logo_in_frame(
    filepaths: tuple[str, ...] | Literal[""],
    frame: ttk.Frame,
    reference: list[ImageTk.PhotoImage],
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
            photo = ImageTk.PhotoImage(img)

            img_label = ttk.Label(frame, image=photo)
            img_label.pack(side=ttk.LEFT, padx=(0, 10))

            reference.append(photo)
        except Exception as e:
            print(f"Error loading image {path}: {e}")
