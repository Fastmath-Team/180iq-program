from typing import Literal

import ttkbootstrap as ttk


class AppInterface:
    def update_logo(self, filepaths: tuple[str, ...] | Literal[""]):
        raise NotImplementedError()

    @property
    def festname(self) -> ttk.StringVar:
        raise NotImplementedError()

    @property
    def history(self) -> ttk.StringVar:
        raise NotImplementedError()
