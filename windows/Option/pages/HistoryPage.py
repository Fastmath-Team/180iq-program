import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus.flowables import Flowable

from interface import AppInterface, Round


# คลาส Builder และ TkBuilder
class Builder:
    def add_text(self, msg: str, *a):
        raise NotImplementedError()


class TkBuilder(Builder):
    def __init__(self, master: tk.Text):
        self._textbox = master

    def add_text(self, msg: str, *a):
        self._textbox.insert("end", msg, *a)


class PdfBuilder(Builder):
    def __init__(self):
        base_styles = getSampleStyleSheet()
        self._styles = {
            "h3": ParagraphStyle(
                "RoundStyle",
                parent=base_styles["h2"],
                fontSize=12,
                leading=14,
                fontName="IBMPlexSansThai-Bold",
            ),
            None: ParagraphStyle(
                "ContentStyle",
                parent=base_styles["Normal"],
                fontName="IBMPlexSansThai-Regular",
            ),
        }
        self._story: list[Flowable] = [
            Paragraph(
                "ประวัติโจทย์และคำตอบ",
                ParagraphStyle(
                    "TitleStyle",
                    parent=base_styles["h1"],
                    fontSize=18,
                    alignment=TA_CENTER,
                    fontName="IBMPlexSansThai-Bold",
                ),
            ),
            Spacer(1, 0.2 * inch),
        ]

    def add_text(self, msg: str, style=None, *a):
        return self._story.append(Paragraph(msg, self._styles[style]))

    def generate(self, file_path: str):
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        doc.build(self._story)


# คลาส TextBuilder สำหรับการสร้างข้อความ
class TextBuilder(Builder):
    def __init__(self):
        self._s = []

    def add_text(self, msg: str, *a):
        self._s.append(msg)

    def get_text(self) -> str:
        return "\n".join(self._s)


def build_field(rounds: list[Round], box: Builder):
    for x, round in enumerate(rounds):
        total_time_in_round = sum(hist.time_per_question for hist in round.items)
        box.add_text(f"รอบที่ {x + 1} [ระยะเวลา {total_time_in_round} วินาที]\n", "h3")

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
            box.add_text(f"{hist.index + 1}: {q} → {a} {d}\n")


class HistoryPage(ctk.CTkFrame):
    def __init__(self, master, app: AppInterface, **kwargs):
        from styles import font as FONT

        super().__init__(master, **kwargs)

        self.app = app
        h = TextBuilder()
        build_field(self.app.rounds, h)
        self.history_text = h.get_text()

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            top_frame, text="ประวัติโจทย์", font=FONT.StaticFont16Bold, anchor="w"
        ).pack(side="left", fill="both", expand=True)

        button_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        button_frame.pack(side="right")

        def copy_text(*_):
            self.clipboard_clear()
            self.clipboard_append(self.history_text)
            messagebox.showinfo("คัดลอกสำเร็จ", "คัดลอกประวัติโจทย์เรียบร้อยแล้ว")

        ctk.CTkButton(button_frame, text="คัดลอก", command=copy_text, width=0).pack(
            side="left", padx=(0, 10)
        )

        ctk.CTkButton(
            button_frame, text="Export PDF", command=self.export_to_pdf, width=0
        ).pack(side="left")

        history_textbox = RichText(self, wrap="word")
        history_textbox.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        textbox_builder = TkBuilder(history_textbox)
        build_field(self.app.rounds, textbox_builder)
        history_textbox.configure(state="disabled")

    def export_to_pdf(self):
        if not self.history_text:
            messagebox.showinfo("ไม่มีข้อมูล", "ไม่พบประวัติโจทย์ที่สามารถ Export ได้")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
            title="บันทึกประวัติเป็น PDF",
        )

        if not file_path:
            return

        try:
            pdf_builder = PdfBuilder()
            build_field(self.app.rounds, pdf_builder)
            pdf_builder.generate(file_path)

            messagebox.showinfo("Export สำเร็จ", f"บันทึกไฟล์ PDF ได้ที่: {file_path}")

        except Exception as e:
            messagebox.showerror("Export ล้มเหลว", f"ไม่สามารถบันทึกไฟล์ PDF ได้: {e}")


# https://stackoverflow.com/a/63105641/2736814
class RichText(ctk.CTkTextbox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        default_font = ctk.CTkFont(weight="normal")
        em = default_font.measure("m")
        default_size = default_font.cget("size")
        bold_font = ctk.CTkFont(weight="bold")
        italic_font = ctk.CTkFont(slant="italic")
        h3_font = ctk.CTkFont(size=int(default_size * 1.5), weight="bold")

        self._textbox.tag_configure("bold", font=bold_font)
        self._textbox.tag_configure("italic", font=italic_font)
        self._textbox.tag_configure("h3", font=h3_font, spacing1=default_size * 0.25)
        lmargin2 = em + default_font.measure("\u2022 ")
        self._textbox.tag_configure("bullet", lmargin1=em, lmargin2=lmargin2)

    def insert_bullet(self, index, text):
        self.insert(index, f"\u2022 {text}", "bullet")

    def configure(self, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        if "state" in cnf:
            return self._textbox.configure(state=cnf["state"])
        return super().configure(cnf, **kw)
