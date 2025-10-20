from __future__ import annotations

import io
import csv
from datetime import datetime
from typing import Tuple

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def _draw_text(c: canvas.Canvas, x: float, y: float, text: str, size: int = 10, color=colors.black) -> None:
    c.setFont("Helvetica", size)
    c.setFillColor(color)
    c.drawString(x, y, text)


def make_pdf_report(df, top_k: int = 20) -> Tuple[bytes, bytes, str]:
    """Render a concise clinician report PDF and a companion CSV of the top_k rows."""
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_name = f"ARISE_Report_{ts}"
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=LETTER)
    W, H = LETTER

    # Header banner
    c.setFillColor(colors.HexColor("#0E2A3E"))
    c.rect(0, H - 70, W, 70, fill=1, stroke=0)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, H - 45, "ARISE — Aging Reversal In-Silico Evaluation")
    c.setFont("Helvetica", 10)
    c.drawString(50, H - 60, "Clinician & Research Summary")

    # Intro text
    y = H - 90
    _draw_text(c, 50, y, "This report ranks virtual therapy candidates by predicted rejuvenation, safety risk, and confidence.")
    y -= 14
    _draw_text(c, 50, y, "Use as hypothesis generation only. Validate with a minimal wet-lab plan.", color=colors.HexColor("#2B7BBB"))

    # Table header
    y -= 26
    headers = ["Rank", "Name", "Type", "Dose", "Pulse(h)", "Target", "Rej.", "Risk↓", "Conf.", "Composite"]
    widths = [35, 110, 90, 50, 60, 80, 45, 45, 45, 60]
    x = 40
    c.setFillColor(colors.HexColor("#2B7BBB"))
    c.setFont("Helvetica-Bold", 10)
    for h, w in zip(headers, widths):
        c.drawString(x, y, h)
        x += w
    y -= 12
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)

    # Rows
    top = df.head(int(top_k)).reset_index(drop=True)
    rank = 1
    for _, r in top.iterrows():
        if y < 80:
            c.showPage()
            y = H - 70
        x = 40
        cells = [
            rank,
            r["name"],
            r["type"],
            f"{r['dose']:.2f}",
            int(r["pulse_hours"]),
            r["target_genes"],
            f"{r['Rejuvenation']:.1f}",
            f"{r['SafetyRisk']:.1f}",
            f"{r['Confidence']:.1f}",
            f"{r['Composite']:.1f}",
        ]
        for val, w in zip(cells, widths):
            c.drawString(x, y, str(val))
            x += w
        y -= 12
        rank += 1

    # Footer
    c.setFillColor(colors.HexColor("#6B7B8C"))
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(40, 40, "ARISE is exploratory. Do not treat scores as clinical advice. © ARISE")
    c.save()
    pdf_bytes = buf.getvalue()

    # CSV alongside
    csv_buf = io.StringIO()
    cols = [
        "name",
        "type",
        "dose",
        "pulse_hours",
        "target_genes",
        "Rejuvenation",
        "SafetyRisk",
        "Confidence",
        "Composite",
    ]
    writer = csv.writer(csv_buf)
    writer.writerow(cols)
    for _, r in top.iterrows():
        writer.writerow([r[c] for c in cols])
    csv_bytes = csv_buf.getvalue().encode("utf-8")
    return pdf_bytes, csv_bytes, out_name

