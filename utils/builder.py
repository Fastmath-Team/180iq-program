from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.platypus.flowables import Flowable

from interface import Round


class Builder:
    def add_text(self, msg: str, *a):
        raise NotImplementedError()


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
