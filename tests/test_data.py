import pandas as pd
import pytest

from data import total_sales, total_orders, monthly_sales_trend


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "date": pd.to_datetime([
            "2024-01-03", "2024-01-10", "2024-02-05", "2024-02-20",
        ]),
        "order_id": ["ORD-001", "ORD-002", "ORD-003", "ORD-004"],
        "product": ["Wireless Earbuds", "Phone Case", "Smart Watch", "USB-C Cable"],
        "category": ["Audio", "Accessories", "Wearables", "Accessories"],
        "region": ["North", "South", "East", "West"],
        "quantity": [2, 3, 1, 5],
        "unit_price": [79.99, 24.99, 299.99, 12.99],
        "total_amount": [159.98, 74.97, 299.99, 64.95],
    })


def test_total_sales(sample_df):
    assert total_sales(sample_df) == pytest.approx(599.89)


def test_total_orders(sample_df):
    assert total_orders(sample_df) == 4


def test_monthly_sales_trend(sample_df):
    result = monthly_sales_trend(sample_df)
    assert list(result["month"].astype(str)) == ["2024-01", "2024-02"]
    assert result["total_amount"].tolist() == pytest.approx([234.95, 364.94])
