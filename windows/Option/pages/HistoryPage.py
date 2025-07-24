import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from interface import AppInterface, Round


class Builder:
    def add_text(self, msg: str, *a):
        raise NotImplementedError()


class TkBuilder(Builder):
    def __init__(self, master: tk.Text):
        self._textbox = master

    def add_text(self, msg: str, *a):
        self._textbox.insert("end", msg, *a)


class TextBuilder(Builder):
    def __init__(self):
        self._s = []

    def add_text(self, msg: str, *a):
        self._s.append(msg)

    def get_text(self) -> str:
        return "\n".join(self._s)


def build_field(rounds: list[Round], box: Builder):
    i = 1

    for x, round in enumerate(rounds):
        box.add_text(f"รอบที่ {x + 1}\n", "h3")

        if len(round.items) == 0:
            box.add_text("ยังไม่ได้เริ่ม\n")

            continue

        for hist in round.items:
            q = " ".join(hist.question)
            a = "".join(hist.answer)

            d = (
                (
                    "[เน้นตัว "
                    + ", ".join(
                        map(lambda x: str(x + 1), hist.highlighted_question_digits)
                    )
                    + "]"
                )
                if hist.highlighted_question_digits
                else ""
            )

            box.add_text(
                f"{hist.index + 1}: {q} -> {a} [เวลา {hist.time_per_question} วินาที] {d}\n"
            )

            i += 1


class HistoryPage(ctk.CTkFrame):
    def __init__(self, master, app: AppInterface, **kwargs):
        from styles import font as FONT

        super().__init__(master, **kwargs)

        h = TextBuilder()

        build_field(app.rounds, h)

        history = h.get_text()

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            top_frame, text="ประวัติโจทย์", font=FONT.StaticFont16Bold, anchor="w"
        ).pack(side="left", fill="both", expand=True)

        def copy_text(*_):
            self.clipboard_clear()
            self.clipboard_append(history)

            messagebox.showinfo("คัดลอกสำเร็จ", "คัดลอกประวัติโจทย์เรียบร้อยแล้ว")

        ctk.CTkButton(top_frame, text="คัดลอก", command=copy_text, width=0).pack(
            side="right", fill="both"
        )

        history_textbox = RichText(self, wrap="word")
        history_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        a = TkBuilder(history_textbox)  # type: ignore

        build_field(app.rounds, a)

        history_textbox.configure(state="disabled")


# https://stackoverflow.com/a/63105641/2736814
class RichText(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = ctk.CTkFont(weight="normal")

        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = ctk.CTkFont(weight="bold")  # type: ignore
        italic_font = ctk.CTkFont(slant="italic")  # type: ignore
        h3_font = ctk.CTkFont(size=int(default_size * 1.5), weight="bold")  # type: ignore

        self._textbox.tag_configure("bold", font=bold_font)
        self._textbox.tag_configure("italic", font=italic_font)
        self._textbox.tag_configure("h3", font=h3_font, spacing1=default_size * 0.25)

        lmargin2 = em + default_font.measure("\u2022 ")
        self._textbox.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f"\u2022 {text}", "bullet")

    def configure(self, cnf=None, **kw):  # type: ignore
        if cnf is None:
            cnf = {}

        if "state" in cnf:
            return self._textbox.configure(state=cnf["state"])

        return super().configure(cnf, **kw)  # type: ignore
