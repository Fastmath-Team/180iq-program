import customtkinter as ctk
import ttkbootstrap as ttk

from components.RoundOptions import RoundOptions
from components.ScrolledFrame import ScrolledFrame


class RoundPage(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padding=10, style="light.TFrame", **kwargs)

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

        self.content_frame = content_frame = ctk.CTkScrollableFrame(self)
        content_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.rounds = [
            RoundOptions(content_frame, on_remove=self.remove_round),
            RoundOptions(content_frame, on_remove=self.remove_round),
            RoundOptions(content_frame, on_remove=self.remove_round),
            RoundOptions(content_frame, on_remove=self.remove_round),
        ]

        for round in self.rounds:
            round.pack(fill="x")

        self._renumber_rounds()

    def _renumber_rounds(self):
        for idx, round in enumerate(self.rounds):
            round.round.set(idx + 1)

    def add_round(self):
        round = RoundOptions(self.content_frame, on_remove=self.remove_round)
        round.pack(fill="x")
        self.rounds.append(round)
        self._renumber_rounds()

    def remove_round(self, item: RoundOptions):
        item.destroy()
        self.rounds.remove(item)
        self._renumber_rounds()
