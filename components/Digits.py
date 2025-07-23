import random
from typing import Literal

import customtkinter as ctk

from styles import colors as COLORS
from styles.theme import THEME


class Digit(ctk.CTkFrame):
    def __init__(self, master, mode: Literal["compact", "full"] = "full", **kwargs):
        from styles import font as FONT

        super().__init__(
            master,
            fg_color="transparent",
            border_color=THEME.CTkFrame.top_fg_color[0],
            border_width=2 if mode == "full" else 0,
            **kwargs,
        )

        self._label = ctk.CTkLabel(
            self,
            text="0",
            font=FONT.Font108Bold,
            anchor="center",
            padx=10 if mode == "full" else 0,
        )

        self._label.pack(padx=10 if mode == "full" else 1, pady=10, expand=True)

    def set_text(self, text: str):
        self._label.configure(text=text)

    def get_text(self) -> str:
        return self._label.cget("text")

    def set_highlight(self, highlight: bool):
        self._label.configure(
            text_color=COLORS.Green if highlight else THEME.CTkLabel.text_color[0]
        )


class Digits(ctk.CTkFrame):
    def __init__(self, master, mode: Literal["compact", "full"] = "full", **kwargs):
        super().__init__(
            master,
            fg_color="transparent"
            if mode == "full"
            else THEME.CTkFrame.top_fg_color[0],
            **kwargs,
        )

        self._mode: Literal["compact", "full"] = mode
        self._digits: list[Digit] = []

        self._spinning_timer_handle: str = ""

    def set_digits(self, digits: list[str]):
        diff = len(digits) - len(self._digits)

        if diff > 0:
            for i in range(diff):
                label = Digit(self, mode=self._mode)

                label.grid(
                    row=0,
                    column=len(self._digits),
                    padx=5,
                )

                self._digits.append(label)

        elif diff < 0:
            for _ in range(-diff):
                label = self._digits.pop()
                label.destroy()

        for digit, label in zip(digits, self._digits):
            label.set_text(f"{digit}")

    def get_digits(self) -> list[str]:
        return [label.get_text() for label in self._digits]

    digits = property(get_digits, set_digits)

    def set_highlighted_digits(self, digits: set[int]):
        for i, label in enumerate(self._digits):
            label.set_highlight(i in digits)

    def start_spinning(self):
        self.stop_spinning()

        self._spinning_timer_handle = self.after(50, self._spin)

    def stop_spinning(self):
        if self._spinning_timer_handle:
            self.after_cancel(self._spinning_timer_handle)

    def _spin(self):
        for label in self._digits:
            label.set_text(random.choice("0123456789"))

        self._spinning_timer_handle = self.after(50, self._spin)
