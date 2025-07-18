import ttkbootstrap as ttk

class Digits(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs, style='light.TFrame')

        self._digits: list[ttk.Label] = []

    def set_digits(self, digits: list[int]):
        diff = len(digits) - len(self._digits)

        if diff > 0:
            for i in range(diff):
                label = ttk.Label(
                    self,
                    text="0",
                    font=("Arial", 108, "bold"),
                    anchor="center",
                    style="display.light.Inverse.TLabel",
                    padding=(10, -10, 10, -10),
                )

                label.grid(row=0, column=len(self._digits))

                self._digits.append(label)

        elif diff < 0:
            for _ in range(-diff):
                label = self._digits.pop()
                label.destroy()

        for digit, label in zip(digits, self._digits):
            label['text'] = f'{digit}'
