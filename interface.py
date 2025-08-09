from dataclasses import dataclass
from typing import Literal


@dataclass
class RoundOptions:
    question_count: int
    time_per_question: int
    question_digit: int | Literal[4, 5]
    answer_digit: int | Literal[2, 3]
    highlighted_question_digits: set[int]


@dataclass(frozen=True)
class QuestionAnswer:
    index: int
    question: list[str]
    answer: list[str]
    time_per_question: int
    highlighted_question_digits: set[int]


@dataclass(frozen=True)
class Round:
    items: list[QuestionAnswer]
    options: RoundOptions


class AppInterface:
    def update_logo(self, size: int | None):
        raise NotImplementedError()

    def save_settings(self):
        raise NotImplementedError()

    def reset_settings(self):
        raise NotImplementedError()

    def export_to_pdf(self, source: Literal["exit", "option"] = "option") -> bool:
        raise NotImplementedError()

    @property
    def version(self) -> str:
        raise NotImplementedError()

    @property
    def logo_filepaths(self) -> tuple[str, ...]:
        raise NotImplementedError()

    @logo_filepaths.setter
    def logo_filepaths(self, filepaths: tuple[str, ...]):
        raise NotImplementedError()

    @property
    def festname(self) -> str:
        raise NotImplementedError()

    @festname.setter
    def festname(self, value: str):
        raise NotImplementedError()

    @property
    def rounds(self) -> list[Round]:
        raise NotImplementedError()

    def trigger_update_rounds(
        self,
        which: Literal[
            "question_digit",
            "answer_digit",
            "highlighted_question_digits",
            "timer",
            "all",
        ],
    ):
        raise NotImplementedError()

    @property
    def current_index(self) -> int:
        raise NotImplementedError()

    @property
    def current_round_index(self) -> int:
        raise NotImplementedError()

    @property
    def current_last(self) -> bool:
        raise NotImplementedError()

    @current_last.setter
    def current_last(self, value: bool):
        raise NotImplementedError()
