import plotly.express as px
import streamlit as st

from data import load_sales_data, total_sales, total_orders, monthly_sales_trend

st.set_page_config(page_title="ShopSmart Sales Dashboard", layout="wide")


@st.cache_data
def get_data():
    return load_sales_data()


try:
    sales_df = get_data()
except Exception as e:
    st.error(f"Failed to load sales data: {e}")
    st.stop()

st.title("ShopSmart Sales Dashboard")

col1, col2 = st.columns(2)
col1.metric("Total Sales", f"${total_sales(sales_df):,.0f}")
col2.metric("Total Orders", f"{total_orders(sales_df):,}")

st.subheader("Sales Trend Over Time")
trend_df = monthly_sales_trend(sales_df)
trend_df["month"] = trend_df["month"].astype(str)
fig_trend = px.line(trend_df, x="month", y="total_amount", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)
