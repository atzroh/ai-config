from inventory import low_stock_items, totalValue

STORE = {"items": [
    {"name": "pen", "price": 100, "stock": 3},
    {"name": "note", "price": 200, "stock": 10},
]}


def test_low_stock_items():
    assert low_stock_items(STORE) == ["pen"]


def test_total_value():
    assert totalValue(STORE) == 2300
