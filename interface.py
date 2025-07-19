from dataclasses import dataclass
from typing import Literal

import ttkbootstrap as ttk

@dataclass
class RoundOptions:
    question_count: int
    time_per_question: int
    question_digit: int | Literal[4, 5]
    answer_digit: int | Literal[2, 3]
    highlighted_question_digits: set[int]

class AppInterface:
    def update_logo(self, filepaths: tuple[str, ...] | Literal[""]):
        raise NotImplementedError()

    @property
    def festname(self) -> str:
        raise NotImplementedError()

    @festname.setter
    def festname(self, value: str):
        raise NotImplementedError()

    @property
    def history(self) -> ttk.StringVar:
        raise NotImplementedError()

    @property
    def round_options(self) -> list[RoundOptions]:
        raise NotImplementedError()
