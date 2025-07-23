import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox

import customtkinter as ctk

from interface import AppInterface, Round

"""
    NOTE
    1. เอา "ประวัติโจทย์" ข้างใน Rich Text ออก
    2. เพิ่มกติกาของแต่ละรอบ (เวลา+เน้นตัวไหน)
    3. ประวัติไม่ทับ แต่ต้องขึ้นข้

        > 1
        > 1234 - 56
        > -> 2
        > <- 1
        > 7777 - 12
        >
        > 1. 1234 - 56
        > 1. 7777 - 12
"""


# i know we can merge these two functions together
def build_text(rounds: list[Round]) -> str:
    s = []
    i = 1

    for x, round in enumerate(rounds):
        s.append(f"รอบที่ {x + 1}")

        if len(round.items) == 0:
            s.append("ยังไม่ได้เริ่ม\n")

            continue

        for hist in round.items:
            q = " ".join(map(str, hist.question))
            s.append(f"{i}: {q} -> {hist.answer}")

            i += 1

    return "\n".join(s)


def build_field(rounds: list[Round], box: tk.Text):
    i = 1

    box.insert("end", "ประวัติโจทย์:\n", "h2")

    for x, round in enumerate(rounds):
        box.insert("end", f"รอบที่ {x + 1}\n", "h3")

        if len(round.items) == 0:
            box.insert("end", "ยังไม่ได้เริ่ม\n")

            continue

        for hist in round.items:
            q = " ".join(hist.question)
            a = "".join(hist.answer)

            box.insert("end", f"{i}: {q} -> {a}\n")

            i += 1


class HistoryPage(ctk.CTkFrame):
    def __init__(self, master, app: AppInterface, **kwargs):
        super().__init__(master, **kwargs)

        history = build_text(app.rounds)

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            top_frame, text="ประวัติโจทย์", font=(None, 16, "bold"), anchor="w"
        ).pack(side="left", fill="both", expand=True)

        def copy_text(*_):
            self.clipboard_clear()
            self.clipboard_append("ประวัติโจทย์:\n" + history)

            messagebox.showinfo("คัดลอกสำเร็จ", "คัดลอกประวัติโจทย์เรียบร้อยแล้ว")

        ctk.CTkButton(top_frame, text="คัดลอก", command=copy_text, width=0).pack(
            side="right", fill="both"
        )

        history_textbox = RichText(self, wrap="word")
        history_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        build_field(app.rounds, history_textbox)  # type: ignore

        history_textbox.configure(state="disabled")


# https://stackoverflow.com/a/63105641/2736814
class RichText(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = tkFont.nametofont("TkTextFont")

        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = tkFont.Font(**default_font.configure())  # type: ignore
        italic_font = tkFont.Font(**default_font.configure())  # type: ignore
        h2_font = tkFont.Font(**default_font.configure())  # type: ignore
        h3_font = tkFont.Font(**default_font.configure())  # type: ignore

        bold_font.configure(weight="bold")
        italic_font.configure(slant="italic")
        h2_font.configure(size=int(default_size * 1.75), weight="bold")
        h3_font.configure(size=int(default_size * 1.5), weight="bold")

        self._textbox.tag_configure("bold", font=bold_font)
        self._textbox.tag_configure("italic", font=italic_font)
        self._textbox.tag_configure("h2", font=h2_font, spacing3=default_size)
        self._textbox.tag_configure("h3", font=h3_font, spacing3=default_size)

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
