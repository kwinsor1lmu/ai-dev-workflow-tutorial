import pandas as pd

CSV_PATH = "data/sales-data.csv"


def load_sales_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    return df


def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)
