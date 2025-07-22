import random

import customtkinter as ctk


class Digits(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            fg_color="transparent",
            border_color="gray10",
            border_width=1,
            **kwargs,
        )

        self._digits: list[ctk.CTkLabel] = []

        self._spinning_timer_handle: str = ""

    def set_digits(self, digits: list[int]):
        diff = len(digits) - len(self._digits)

        if diff > 0:
            for i in range(diff):
                label = ctk.CTkLabel(
                    self,
                    text="0",
                    font=("Arial", 108, "bold"),
                    anchor="center",
                    padx=10,
                )

                label.grid(row=0, column=len(self._digits), padx=10)

                self._digits.append(label)

        elif diff < 0:
            for _ in range(-diff):
                label = self._digits.pop()
                label.destroy()

        for digit, label in zip(digits, self._digits):
            label.configure(text=f"{digit}")

    def get_digits(self) -> list[int]:
        return [int(label['text']) for label in self._digits]

    digits = property(get_digits, set_digits)

    def set_highlighted_digits(self, digits: set[int]):
        for i, label in enumerate(self._digits):
            label.configure(fg_color="yellow2" if i in digits else "transparent")

    def start_spinning(self):
        self.stop_spinning()

        self._spinning_timer_handle = self.after(50, self._spin)

    def stop_spinning(self):
        if self._spinning_timer_handle:
            self.after_cancel(self._spinning_timer_handle)

    def _spin(self):
        for label in self._digits:
            label.configure(text=random.choice("0123456789"))

        self._spinning_timer_handle = self.after(50, self._spin)
