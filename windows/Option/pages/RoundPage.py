import customtkinter as ctk
import ttkbootstrap as ttk

from components.RoundOptions import RoundOptionFrame
from interface import AppInterface, Round, RoundOptions


class RoundPage(ttk.Frame):
    def __init__(self, master, app: AppInterface, **kwargs):
        super().__init__(master, padding=10, style="light.TFrame", **kwargs)

        self._rounds = app.rounds

        input_frame = ttk.Frame(self)
        input_frame.pack(fill="x")

        ttk.Label(
            input_frame,
            text="รอบการแข่งขัน",
            style="light.Inverse.TLabel",
        ).pack(side="left", fill="both", expand=True)

        ttk.Button(
            input_frame, text="เพิ่มรอบการแข่งขัน", style="TButton", command=self.add_round
        ).pack(side="right", fill="both")

        self._content_frame = content_frame = ctk.CTkScrollableFrame(self)
        content_frame.pack(fill="both", expand=True, pady=(10, 0))

        self._round_frames = rounds = [
            RoundOptionFrame(
                content_frame,

                index=i,
                round=round,

                on_remove=self.remove_round
            )
            for i, round in enumerate(app.rounds)
        ]

        for round in rounds:
            round.pack(fill="x")

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
                highlighted_question_digits=set()
            ),
        )

        round_frame = RoundOptionFrame(
            self._content_frame,

            index=len(self._round_frames),
            round=round,

            on_remove=self.remove_round
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
