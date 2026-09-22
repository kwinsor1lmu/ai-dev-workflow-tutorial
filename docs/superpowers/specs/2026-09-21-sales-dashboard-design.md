# Design: E-Commerce Sales Dashboard

Based on `prd/ecommerce-analytics.md`. Covers Phase 1 only (matches `TASKS.md` TASK-1 through TASK-7).

## Overview

A single-page Streamlit dashboard that loads `data/sales-data.csv` and displays two KPI cards (Total Sales, Total Orders), a monthly sales trend line chart, and category/region bar charts, laid out per the PRD's mockup.

## Architecture

Two Python files at the project root, plus a tests directory:

- **`data.py`** — pure data functions (CSV loading + all aggregations). No Streamlit imports. Fully unit-testable in isolation.
- **`app.py`** — Streamlit entry point. Calls `data.py` functions and renders the UI (KPI cards + Plotly charts) directly.
- **`tests/test_data.py`** — pytest tests for every function in `data.py`, using a small in-memory fixture DataFrame.

Dependencies are managed with a plain virtual environment (`venv/`) and `requirements.txt` (streamlit, pandas, plotly, pytest) — no uv or conda.

This two-file split satisfies the "calculations in their own module with tests" requirement without over-fragmenting a small app. A more modular split (separate `charts.py` for Plotly figure builders) was considered and rejected as unnecessary indirection for ~3 charts.

## Components & Data Flow

### `data.py`

- `load_sales_data() -> pd.DataFrame` — reads `data/sales-data.csv`, parses `date` as datetime. Raises on failure; the caller (`app.py`) handles it. `total_amount` is trusted as-is (not recomputed/validated against `quantity × unit_price`) — out of scope for Phase 1.
- `total_sales(df) -> float` — sum of `total_amount`.
- `total_orders(df) -> int` — count of rows (one row per transaction/order).
- `monthly_sales_trend(df) -> pd.DataFrame` — grouped by calendar month, columns `month` and `total_amount`, sorted chronologically. Monthly granularity chosen over daily for a readable trend line matching the PRD mockup.
- `sales_by_category(df) -> pd.DataFrame` — grouped by `category`, summed `total_amount`, sorted descending.
- `sales_by_region(df) -> pd.DataFrame` — grouped by `region`, summed `total_amount`, sorted descending.

### `app.py`

1. Call `load_sales_data()` wrapped in `try/except`. On failure: `st.error(...)` with a clear message, then `st.stop()`.
2. Wrap the load call with `@st.cache_data` to keep repeat loads fast (supports NFR-1's 5-second load target).
3. Render, top to bottom, matching the PRD mockup:
   - Page title ("ShopSmart Sales Dashboard" or similar)
   - Two KPI columns: Total Sales (currency-formatted, `$X,XXX,XXX`) and Total Orders (comma-separated integer)
   - Full-width Plotly line chart: monthly sales trend, with interactive tooltips
   - Two side-by-side Plotly bar charts: sales by category and sales by region, both sorted descending, both with interactive tooltips

No sidebar, no tabs, no filtering controls (Phase 2 scope, explicitly out).

## Error Handling

Missing or unreadable CSV: caught once at load time in `app.py`, surfaced via `st.error()`, and the app halts with `st.stop()`. No retries, no fallback data — matches the PRD's Phase 1 simplicity. Everything downstream (`data.py` aggregation functions) assumes a valid, already-loaded DataFrame and does no defensive validation of its own.

## Testing

`tests/test_data.py` defines one small fixture DataFrame (a handful of hand-crafted rows spanning 2+ months, 2+ categories, 2+ regions) with hand-computed expected results. Tests cover:

- `total_sales` — correct sum
- `total_orders` — correct count
- `monthly_sales_trend` — correct grouping and chronological sort
- `sales_by_category` — correct grouping and descending sort
- `sales_by_region` — correct grouping and descending sort

`load_sales_data()` itself is not tested (no fixture CSV file) — it's a thin Pandas read wrapped in one `try/except`, and `app.py`'s UI code is not tested — standard for a small Streamlit app; it's a thin wiring layer over tested functions.

## Out of Scope (Phase 2, per PRD)

User authentication, database integration, export functionality, email alerts, filtering/date ranges, drill-down, mobile-responsive design, automated refresh.

## Milestone Mapping

This design covers all of `TASKS.md`'s milestones:

- TASK-1: Environment setup (venv, requirements.txt, project skeleton)
- TASK-2: `data.py` — `load_sales_data()`
- TASK-3: KPI cards in `app.py`
- TASK-4: Monthly trend chart
- TASK-5: Category/region bar charts
- TASK-6: Testing and refinement (pytest suite + acceptance criteria verification)
- TASK-7: Deployment (executed by the user, not part of this implementation plan)
