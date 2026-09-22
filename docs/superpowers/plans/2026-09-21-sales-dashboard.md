# Sales Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the Phase 1 Streamlit sales dashboard described in `prd/ecommerce-analytics.md` — KPI cards, monthly trend chart, category/region breakdowns — reading from `data/sales-data.csv`.

**Architecture:** Two Python files at the project root (`data.py` for pure, tested aggregation functions; `app.py` for the Streamlit UI that calls them) plus `tests/test_data.py`. Dependencies in a plain `venv/` virtual environment via `requirements.txt`.

**Tech Stack:** Python 3.11+, Streamlit, Pandas, Plotly, pytest.

**Spec:** `docs/superpowers/specs/2026-09-21-sales-dashboard-design.md`

## Global Constraints

- Work directly on the current git branch (`feature/sales-dashboard`) — do not create a worktree.
- Use a plain Python virtual environment in `venv/` with `requirements.txt` for dependencies — no uv, no conda.
- Keep data calculations in their own module (`data.py`), covered by pytest tests.
- Keep code simple and readable.
- `total_amount` in the CSV is trusted as-is — do not recompute or validate it against `quantity × unit_price`.
- Sales trend uses monthly granularity, not daily.
- No sidebar, tabs, filtering, authentication, or export functionality — Phase 1 scope only, per the PRD.

## Task-to-Milestone Mapping

This plan's own tasks are numbered independently (Plan Task 1, 2, 3, ...) from the milestones in `TASKS.md` (TASK-1, TASK-2, ...). Each plan task below is labeled with the milestone it belongs to. Plan Task 7 (deployment) is the exception — it is not implemented here; it hands off to the user.

---

### Plan Task 1 — [TASK-1] Environment setup and project initialization

**Files:**
- Create: `requirements.txt`
- Create: `app.py`

**Interfaces:**
- Produces: a runnable (empty/placeholder) Streamlit app at `app.py`, and an activated `venv/` with all dependencies installed, for every later task to build on.

- [ ] **Step 1: Create the virtual environment**

Run: `python -m venv venv`

- [ ] **Step 2: Activate it and write requirements.txt**

Create `requirements.txt`:

```
streamlit
pandas
plotly
pytest
```

- [ ] **Step 3: Install dependencies**

Windows (PowerShell): `venv\Scripts\pip install -r requirements.txt`

Confirm it completes with no errors.

- [ ] **Step 4: Create a placeholder app.py**

```python
import streamlit as st

st.title("ShopSmart Sales Dashboard")
st.write("Dashboard under construction.")
```

- [ ] **Step 5: Verify the app launches**

Run: `venv\Scripts\streamlit run app.py`

Expected: browser opens (or a local URL is printed) showing the title and placeholder text, with no errors in the terminal. Stop the server (Ctrl+C) after confirming.

- [ ] **Step 6: Commit**

```bash
git add requirements.txt app.py
git commit -m "TASK-1: Set up project environment and placeholder app"
```

---

### Plan Task 2 — [TASK-2] Data loading in data.py

**Files:**
- Create: `data.py`

**Interfaces:**
- Produces: `load_sales_data() -> pd.DataFrame` with columns `date` (datetime64), `order_id`, `product`, `category`, `region` (str/object), `quantity` (int), `unit_price` (float), `total_amount` (float). Raises an exception (whatever `pandas.read_csv` raises) if `data/sales-data.csv` is missing or malformed — the caller in Plan Task 3 handles this.

- [ ] **Step 1: Write load_sales_data()**

```python
import pandas as pd

CSV_PATH = "data/sales-data.csv"


def load_sales_data() -> pd.DataFrame:
    df = pd.read_csv(CSV_PATH, parse_dates=["date"])
    return df
```

- [ ] **Step 2: Verify it loads the real data correctly**

Run this one-off check (no pytest — per the spec, `load_sales_data()` has no automated test since there's no fixture CSV):

```bash
venv\Scripts\python -c "from data import load_sales_data; df = load_sales_data(); print(len(df)); print(df.dtypes)"
```

Expected: prints `482` and shows `date` as `datetime64[ns]`, `quantity` as `int64`, `unit_price`/`total_amount` as `float64`, the rest as `object`.

- [ ] **Step 3: Commit**

```bash
git add data.py
git commit -m "TASK-2: Add data loading module"
```

---

### Plan Task 3 — [TASK-3] KPI cards implementation

**Files:**
- Modify: `data.py`
- Modify: `app.py`
- Create: `tests/test_data.py`

**Interfaces:**
- Consumes: `load_sales_data()` from Plan Task 2.
- Produces: `total_sales(df: pd.DataFrame) -> float`, `total_orders(df: pd.DataFrame) -> int` in `data.py`, used directly by later tasks and by `app.py`'s KPI rendering.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_data.py`:

```python
import pandas as pd
import pytest

from data import total_sales, total_orders


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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `venv\Scripts\pytest tests/test_data.py -v`

Expected: FAIL with `ImportError: cannot import name 'total_sales'` (and `total_orders`).

- [ ] **Step 3: Implement total_sales and total_orders**

Add to `data.py`:

```python
def total_sales(df: pd.DataFrame) -> float:
    return df["total_amount"].sum()


def total_orders(df: pd.DataFrame) -> int:
    return len(df)
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv\Scripts\pytest tests/test_data.py -v`

Expected: both tests PASS.

- [ ] **Step 5: Render the KPI cards in app.py**

Replace the placeholder body of `app.py` with:

```python
import streamlit as st

from data import load_sales_data, total_sales, total_orders

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
```

- [ ] **Step 6: Verify the app runs and shows correct KPIs**

Run: `venv\Scripts\streamlit run app.py`

Expected: page shows "Total Sales" formatted as `$116,...` and "Total Orders" as `482`, no errors.

- [ ] **Step 7: Commit**

```bash
git add data.py app.py tests/test_data.py
git commit -m "TASK-3: Add KPI cards for total sales and total orders"
```

---

### Plan Task 4 — [TASK-4] Sales trend chart

**Files:**
- Modify: `data.py`
- Modify: `app.py`
- Modify: `tests/test_data.py`

**Interfaces:**
- Consumes: `sample_df` fixture from Plan Task 3's `tests/test_data.py`.
- Produces: `monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame` in `data.py`, with columns `month` (Period or Timestamp, chronologically sorted) and `total_amount` (float, summed per month). Used by `app.py` to build the line chart.

- [ ] **Step 1: Write the failing test**

Add to `tests/test_data.py`:

```python
from data import monthly_sales_trend


def test_monthly_sales_trend(sample_df):
    result = monthly_sales_trend(sample_df)
    assert list(result["month"].astype(str)) == ["2024-01", "2024-02"]
    assert result["total_amount"].tolist() == pytest.approx([234.95, 364.94])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `venv\Scripts\pytest tests/test_data.py -v`

Expected: FAIL with `ImportError: cannot import name 'monthly_sales_trend'`.

- [ ] **Step 3: Implement monthly_sales_trend**

Add to `data.py`:

```python
def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    monthly = (
        df.groupby(df["date"].dt.to_period("M"))["total_amount"]
        .sum()
        .reset_index()
        .rename(columns={"date": "month"})
        .sort_values("month")
    )
    return monthly
```

- [ ] **Step 4: Run test to verify it passes**

Run: `venv\Scripts\pytest tests/test_data.py -v`

Expected: PASS.

- [ ] **Step 5: Add the line chart to app.py**

Add near the top of `app.py`:

```python
import plotly.express as px

from data import load_sales_data, total_sales, total_orders, monthly_sales_trend
```

Append after the KPI columns block:

```python
st.subheader("Sales Trend Over Time")
trend_df = monthly_sales_trend(sales_df)
trend_df["month"] = trend_df["month"].astype(str)
fig_trend = px.line(trend_df, x="month", y="total_amount", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)
```

- [ ] **Step 6: Verify the chart renders**

Run: `venv\Scripts\streamlit run app.py`

Expected: a line chart appears below the KPIs showing 12 monthly points, with hover tooltips showing exact values, no errors.

- [ ] **Step 7: Commit**

```bash
git add data.py app.py tests/test_data.py
git commit -m "TASK-4: Add monthly sales trend chart"
```

---

### Plan Task 5 — [TASK-5] Category and region breakdowns

**Files:**
- Modify: `data.py`
- Modify: `app.py`
- Modify: `tests/test_data.py`

**Interfaces:**
- Consumes: `sample_df` fixture from `tests/test_data.py`.
- Produces: `sales_by_category(df: pd.DataFrame) -> pd.DataFrame` and `sales_by_region(df: pd.DataFrame) -> pd.DataFrame` in `data.py`, each with columns `category`/`region` and `total_amount`, sorted descending by `total_amount`. Used by `app.py` for the two bar charts.

- [ ] **Step 1: Write the failing tests**

Add to `tests/test_data.py`:

```python
from data import sales_by_category, sales_by_region


def test_sales_by_category(sample_df):
    result = sales_by_category(sample_df)
    assert result["category"].tolist() == ["Wearables", "Audio", "Accessories"]
    assert result["total_amount"].tolist() == pytest.approx([299.99, 159.98, 139.92])


def test_sales_by_region(sample_df):
    result = sales_by_region(sample_df)
    assert result["region"].tolist() == ["East", "North", "South", "West"]
    assert result["total_amount"].tolist() == pytest.approx([299.99, 159.98, 74.97, 64.95])
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `venv\Scripts\pytest tests/test_data.py -v`

Expected: FAIL with `ImportError` for `sales_by_category` and `sales_by_region`.

- [ ] **Step 3: Implement sales_by_category and sales_by_region**

Add to `data.py`:

```python
def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("category")["total_amount"]
        .sum()
        .reset_index()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("region")["total_amount"]
        .sum()
        .reset_index()
        .sort_values("total_amount", ascending=False)
        .reset_index(drop=True)
    )
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `venv\Scripts\pytest tests/test_data.py -v`

Expected: all tests PASS.

- [ ] **Step 5: Add the bar charts to app.py**

Update the import line:

```python
from data import (
    load_sales_data,
    total_sales,
    total_orders,
    monthly_sales_trend,
    sales_by_category,
    sales_by_region,
)
```

Append after the trend chart block:

```python
st.subheader("Breakdowns")
col3, col4 = st.columns(2)

with col3:
    st.write("Sales by Category")
    category_df = sales_by_category(sales_df)
    fig_category = px.bar(category_df, x="category", y="total_amount")
    st.plotly_chart(fig_category, use_container_width=True)

with col4:
    st.write("Sales by Region")
    region_df = sales_by_region(sales_df)
    fig_region = px.bar(region_df, x="region", y="total_amount")
    st.plotly_chart(fig_region, use_container_width=True)
```

- [ ] **Step 6: Verify both charts render**

Run: `venv\Scripts\streamlit run app.py`

Expected: two side-by-side bar charts, category chart showing 5 bars with Electronics tallest, region chart showing 4 bars, both sorted descending, hover tooltips work, no errors.

- [ ] **Step 7: Commit**

```bash
git add data.py app.py tests/test_data.py
git commit -m "TASK-5: Add category and region breakdown charts"
```

---

### Plan Task 6 — [TASK-6] Testing and refinement

**Files:**
- Modify: `app.py` (polish only — labels, spacing; no new data functions)

**Interfaces:**
- Consumes: everything produced in Plan Tasks 2–5.
- Produces: nothing new — this task verifies and polishes the existing app.

- [ ] **Step 1: Run the full pytest suite**

Run: `venv\Scripts\pytest tests/ -v`

Expected: all tests PASS, no warnings.

- [ ] **Step 2: Verify acceptance criteria against the PRD's expected output**

Run: `venv\Scripts\streamlit run app.py` and manually confirm against `prd/ecommerce-analytics.md`'s "Expected Output" table:

- Total Sales ≈ $116,500
- Total Orders = 482
- Top category (tallest bar) = Electronics
- Regions shown = North, South, East, West
- No errors or warnings in the terminal or browser

- [ ] **Step 3: Polish labels and layout for executive presentation**

In `app.py`, review and tighten: chart titles (e.g., pass `title="Sales by Category"` to `px.bar`/`px.line` calls instead of relying solely on `st.write`/`st.subheader`), axis labels (`labels={"total_amount": "Total Sales ($)"}` on each Plotly call), and confirm the KPI/chart order matches the PRD mockup (KPIs → trend → category/region side-by-side).

- [ ] **Step 4: Re-run the app to confirm polish didn't break anything**

Run: `venv\Scripts\streamlit run app.py`

Expected: same data as Step 2, now with clearer titles/labels, no errors.

- [ ] **Step 5: Re-run the full test suite one more time**

Run: `venv\Scripts\pytest tests/ -v`

Expected: all tests still PASS.

- [ ] **Step 6: Commit**

```bash
git add app.py
git commit -m "TASK-6: Polish labels and verify acceptance criteria"
```

---

### Plan Task 7 — [TASK-7] Deployment (hand-off to user — not executed as part of this plan)

This task is **not implemented by the plan's executor**. Once Plan Tasks 1–6 are complete, reviewed, and merged into `main`, deployment is the user's own step:

1. Merge `feature/sales-dashboard` into `main` (via PR review, per your normal process).
2. From `main`, go to Streamlit Community Cloud, connect the GitHub repo, and deploy `app.py`.
3. Confirm the public URL loads the dashboard within 5 seconds (NFR-1) with no errors.
4. Update `TASKS.md`'s TASK-7 checkboxes and Commit line yourself once deployed.

No further plan steps follow this one.
