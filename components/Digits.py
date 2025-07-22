import random

import customtkinter as ctk


class Digits(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

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

                label.grid(row=0, column=len(self._digits))

                self._digits.append(label)

        elif diff < 0:
            for _ in range(-diff):
                label = self._digits.pop()
                label.destroy()

        for digit, label in zip(digits, self._digits):
            label.configure(text=f"{digit}")

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
