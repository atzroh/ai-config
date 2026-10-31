from report import build_sales_report

CSV = """date,item,qty,price
2026-10-01, Apple ,3,100
2026-10-01,banana,2,50
2026-10-02,apple,1,100
"""


def write_csv(tmp_path):
    p = tmp_path / "sales.csv"
    p.write_text(CSV, encoding="utf-8")
    return p


def test_report_without_tax(tmp_path):
    out = tmp_path / "out.txt"
    text = build_sales_report(write_csv(tmp_path), out, False, False)
    assert "apple: 400" in text
    assert "banana: 100" in text
    assert "TOTAL: 500" in text
    assert out.read_text(encoding="utf-8") == text


def test_report_with_tax(tmp_path):
    out = tmp_path / "out.txt"
    text = build_sales_report(write_csv(tmp_path), out, True, False)
    assert "apple: 440" in text
    assert "TOTAL: 550" in text


def test_big_sales_note(tmp_path):
    p = tmp_path / "big.csv"
    p.write_text("date,item,qty,price\n2026-10-03,tv,2,60000\n", encoding="utf-8")
    text = build_sales_report(p, tmp_path / "out.txt", False, False)
    assert "NOTE: big sales day" in text
