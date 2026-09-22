import pandas as pd
import pytest

from data import (
    total_sales,
    total_orders,
    monthly_sales_trend,
    sales_by_category,
    sales_by_region,
)


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


def test_sales_by_category(sample_df):
    result = sales_by_category(sample_df)
    assert result["category"].tolist() == ["Wearables", "Audio", "Accessories"]
    assert result["total_amount"].tolist() == pytest.approx([299.99, 159.98, 139.92])


def test_sales_by_region(sample_df):
    result = sales_by_region(sample_df)
    assert result["region"].tolist() == ["East", "North", "South", "West"]
    assert result["total_amount"].tolist() == pytest.approx([299.99, 159.98, 74.97, 64.95])
