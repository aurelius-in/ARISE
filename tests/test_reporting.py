from src.core.pipeline import run_simulation
from src.core.reporting import make_pdf_report


def test_make_pdf_report_outputs_bytes_and_csv_rows():
    df = run_simulation(n=40, seed=123)
    top_k = 10
    pdf_bytes, csv_bytes, out_name = make_pdf_report(df, top_k=top_k)

    # PDF has non-trivial size
    assert isinstance(pdf_bytes, (bytes, bytearray))
    assert len(pdf_bytes) > 800  # small but non-zero PDF

    # CSV has header + top_k rows
    csv_text = csv_bytes.decode("utf-8")
    lines = [ln for ln in csv_text.splitlines() if ln.strip()]
    assert lines[0].startswith("name,type,dose,pulse_hours,target_genes")
    assert len(lines) == top_k + 1


