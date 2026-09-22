# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A student project built as part of an AI-assisted development workflow tutorial (see `README.md`). The deliverable is a Streamlit sales dashboard built from `prd/ecommerce-analytics.md` (the PRD), tracked milestone-by-milestone in `TASKS.md`, with the implementation plan in `docs/superpowers/plans/2026-09-21-sales-dashboard.md` and the design in `docs/superpowers/specs/2026-09-21-sales-dashboard-design.md`. Read those three files together before making non-trivial changes — the PRD has the requirements, `TASKS.md` has the milestone-to-commit history, and the plan/spec have the "why" behind the current architecture.

## Commands

Windows/PowerShell environment. A plain `venv/` virtual environment is used (no uv, no conda).

```powershell
# Set up (already done; re-run only if venv/ is missing)
python -m venv venv
venv\Scripts\pip install -r requirements.txt

# Run the app
venv\Scripts\streamlit run app.py
```

`streamlit run` in a non-interactive shell hits Streamlit's first-run email prompt and fails (exit 127). Use `--server.headless true` to skip it — this is how the app is verified in this repo, not just a dev convenience:

```powershell
venv\Scripts\streamlit run app.py --server.headless true
```

```powershell
# Run all tests
venv\Scripts\pytest tests/ -v

# Run a single test
venv\Scripts\pytest tests/test_data.py::test_total_sales -v
```

A one-off manual check (no pytest fixture exists for the real CSV):

```powershell
venv\Scripts\python -c "from data import load_sales_data; df = load_sales_data(); print(len(df))"
```

## Architecture

Two files at the project root plus one test file — deliberately not split further (a `charts.py` for Plotly figure builders was considered and rejected as unnecessary for ~3 charts):

- **`data.py`** — pure, Streamlit-free data functions: `load_sales_data()`, `total_sales()`, `total_orders()`, `monthly_sales_trend()`, `sales_by_category()`, `sales_by_region()`. Every function here is covered by `tests/test_data.py` against a small hand-computed fixture DataFrame — not the real CSV. `total_amount` is trusted as-is; it is never recomputed or validated against `quantity × unit_price`.
- **`app.py`** — the Streamlit UI. Loads data once via `@st.cache_data`, wraps the load in `try/except` with `st.error()` + `st.stop()` on failure, and renders top to bottom: title → KPI columns → trend line chart → category/region bar charts side by side. It contains no calculation logic of its own — everything numeric comes from `data.py`.
- **`conftest.py`** (empty, at repo root) — exists only so pytest adds the repo root to `sys.path`; without it, `tests/test_data.py` (which has no `__init__.py` in `tests/`) cannot `from data import ...`. Don't remove it.

## Project conventions specific to this repo

- **Milestone traceability**: every commit message is prefixed with its `TASKS.md` milestone ID (e.g. `TASK-4: Add monthly sales trend chart`). `TASKS.md` has three sections — To Do / In Progress / Done — and moving a task to Done means adding its commit hash and a `Notes:` line (or `clean` if there were no deviations) under that task's entry. Update the board in a separate commit from the implementation commit.
- **Branch**: work happens directly on `feature/sales-dashboard` off `main` — no worktrees.
- **Phase 1 scope only**: no sidebar, tabs, filtering, authentication, or export. Those are explicitly out of scope per the PRD's Phase 2 section; don't add them unless the PRD/TASKS.md changes first.
- **TDD on `data.py`**: new aggregation functions get a failing test in `tests/test_data.py` first, then the implementation, per the plan's task breakdown.
- **Expected values for the real dataset** (`data/sales-data.csv`, 482 rows): Total Sales ≈ $116,500, Total Orders = 482, top category = Electronics, regions = North/South/East/West. Use these to sanity-check changes to `data.py`.
- **Deployment (TASK-7)** is out of scope for implementation work in this repo — it's a manual hand-off to Streamlit Community Cloud performed by the user after merging to `main`, not something to automate or script.

## Lessons

Distilled from the `Notes:` lines in `TASKS.md`'s Done section:

- Don't run `streamlit run` without `--server.headless true` in a non-interactive shell — it hits Streamlit's first-run email prompt and fails with exit 127.
- Don't chase exact dtype strings when checking a loaded DataFrame — this pandas version reports `str`/`datetime64[us]` where older docs/examples say `object`/`datetime64[ns]`. They're semantically equivalent; verify behavior, not the dtype repr.
- Before marking any task done, verify calculated values against the real `data/sales-data.csv`, not just the `tests/test_data.py` fixture — the fixture only proves the aggregation logic is correct, not that it matches the PRD's expected output.
