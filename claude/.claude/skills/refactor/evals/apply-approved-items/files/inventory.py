def _get_items(store):
    # store から items を取り出して返す
    return store["items"]


def low_stock_items(store):
    # 在庫が少ない商品を探す関数です。在庫数が5未満の商品を少ないとみなします。
    # 結果はリストで返します。
    result = []
    for item in _get_items(store):
        if item["stock"] < 5:
            result.append(item["name"])
    return result


def totalValue(store):
    total = 0
    for item in _get_items(store):
        # 価格に在庫数をかける
        total += item["price"] * item["stock"]
    return total
