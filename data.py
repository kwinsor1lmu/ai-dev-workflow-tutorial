import pandas as pd

CSV_PATH = "data/sales-data.csv"


def load_sales_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    return df


def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)


def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby(df["date"].dt.to_period("M"))["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"date": "month"})
        .sort_values("month")
    )
    return monthly
