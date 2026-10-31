import csv


def open_csv(path):
    return open(path, newline="", encoding="utf-8")


def read_file(path):
    # read_file は open_csv を呼び出してファイルを開く関数です
    return open_csv(path)


def getTotal(rows):
    total = 0
    for r in rows:
        total += r["amount"]
    return total


def build_sales_report(path, out_path, include_tax, verbose):
    # ここではファイルを開いてCSVを読み込みます。CSVにはdate, item, qty, priceの列があります。
    # 読み込んだ行はリストに入れていきます。
    f = read_file(path)
    reader = csv.DictReader(f)
    rowList = []
    for row in reader:
        # qtyを整数に変換する
        q = int(row["qty"])
        # priceを整数に変換する
        p = int(row["price"])
        # amountを計算する
        amt = q * p
        if include_tax:
            # 税込みにする
            amt = int(amt * 1.1)
        d = row["date"]
        # 日付を YYYY/MM/DD に変換する
        parts = d.split("-")
        d2 = parts[0] + "/" + parts[1] + "/" + parts[2]
        rowList.append({"date": d2, "item": row["item"].strip().lower(), "amount": amt})
    f.close()

    # 商品ごとに集計する
    by_item = {}
    for r in rowList:
        if r["item"] in by_item:
            by_item[r["item"]] = by_item[r["item"]] + r["amount"]
        else:
            by_item[r["item"]] = r["amount"]

    total = getTotal(rowList)

    # レポートの文字列を作る
    lines = []
    lines.append("Sales Report")
    lines.append("=" * 20)
    for name in sorted(by_item):
        lines.append(name + ": " + str(by_item[name]))
    lines.append("-" * 20)
    lines.append("TOTAL: " + str(total))
    if total > 100000:
        lines.append("NOTE: big sales day")
    text = "\n".join(lines) + "\n"

    # ファイルに書き出す
    with open(out_path, "w", encoding="utf-8") as out:
        out.write(text)
    if verbose:
        print("wrote " + out_path)
    return text
