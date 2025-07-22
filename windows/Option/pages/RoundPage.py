import customtkinter as ctk

from components.RoundOptions import RoundOptionFrame
from interface import AppInterface, Round, RoundOptions


class RoundPage(ctk.CTkFrame):
    def __init__(self, master, app: AppInterface, **kwargs):
        super().__init__(master, **kwargs)

        self._rounds = app.rounds

        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(input_frame, text="รอบการแข่งขัน", anchor="w").pack(
            side="left", fill="both", expand=True
        )

        ctk.CTkButton(input_frame, text="เพิ่มรอบการแข่งขัน", command=self.add_round).pack(
            side="right", fill="both"
        )

        self._content_frame = content_frame = ctk.CTkScrollableFrame(self)
        content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self._round_frames = rounds = [
            RoundOptionFrame(
                content_frame, index=i, round=round, on_remove=self.remove_round
            )
            for i, round in enumerate(app.rounds)
        ]

        for round in rounds:
            round.pack(fill="x", padx=(5, 0), pady=5)

        self._renumber_rounds()

    def _renumber_rounds(self):
        can_delete = len(self._rounds) > 1

        for idx, round in enumerate(self._round_frames):
            round.set_index(idx, can_delete)

    def add_round(self):
        round = Round(
            items=[],
            options=RoundOptions(
                question_count=10,
                time_per_question=30,
                question_digit=4,
                answer_digit=2,
                highlighted_question_digits=set(),
            ),
        )

        round_frame = RoundOptionFrame(
            self._content_frame,
            index=len(self._round_frames),
            round=round,
            on_remove=self.remove_round,
        )
        round_frame.pack(fill="x")

        self._round_frames.append(round_frame)
        self._rounds.append(round)

        self._renumber_rounds()

    def remove_round(self, i: int):
        self._rounds.pop(i)

        item = self._round_frames.pop(i)
        item.destroy()

        self._renumber_rounds()
