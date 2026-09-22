# Tasks

This file tracks all work for the e-commerce analytics dashboard.

## Definition of Done

- Acceptance criteria met
- App runs locally with `streamlit run app.py`
- Changes committed with the milestone ID in the message

## To Do

### TASK-5: Category and region breakdowns
Build bar charts showing sales by category and by region.
- [ ] Category bar chart shows all 5 categories, sorted by sales value descending
- [ ] Region bar chart shows all 4 regions, sorted by sales value descending
- [ ] Both charts have interactive tooltips with exact values

Commit:

### TASK-6: Testing and refinement
Verify the dashboard against the PRD's acceptance criteria and polish the presentation.
- [ ] Dashboard runs with no errors or warnings
- [ ] All values verified against expected output (~$116,500 total sales, 482 orders, Electronics top category)
- [ ] Layout and labels reviewed for a professional, executive-presentation-ready appearance

Commit:

### TASK-7: Deployment to Streamlit Community Cloud
Deploy the finished dashboard and confirm public access.
- [ ] App deployed to Streamlit Community Cloud
- [ ] Public shareable URL loads the dashboard without errors
- [ ] Dashboard loads within 5 seconds on the deployed URL

Commit:

## In Progress

## Done

### TASK-1: Environment setup and project initialization
Set up the Python project structure, dependencies, and folders needed to build the dashboard.
- [x] Project structure created (app.py, data/ folder, requirements.txt)
- [x] Dependencies (streamlit, pandas, plotly) install and import without errors
- [x] `streamlit run app.py` launches a blank/placeholder app

Commit: e5caa22
Notes: First `streamlit run app.py` attempt hit Streamlit's interactive first-run email prompt and failed (exit 127) in this non-interactive shell; verified startup instead with `--server.headless true`. No other deviations.

### TASK-2: Data loading and basic structure
Load sales-data.csv with Pandas and validate its structure.
- [x] CSV loads into a DataFrame with correct column types (date, numeric, categorical)
- [x] Row count matches expected 482 records
- [x] Basic error handling for missing/malformed file

Commit: f3000f3
Notes: pandas reports dtypes as `str`/`datetime64[us]` rather than `object`/`datetime64[ns]` (newer pandas default) — semantically equivalent, satisfies the interface contract.

### TASK-3: KPI cards implementation
Display Total Sales and Total Orders as formatted KPI cards.
- [x] Total Sales calculated correctly and formatted as currency ($X,XXX,XXX)
- [x] Total Orders calculated correctly with number formatting
- [x] KPIs displayed prominently at the top of the dashboard

Commit: f8896da
Notes: clean

### TASK-4: Sales trend chart
Build a line chart showing sales over time.
- [x] Line chart renders sales trend with time on the X-axis and sales amount on the Y-axis
- [x] Interactive tooltips show exact values
- [x] Chart data matches expected calculations from the CSV

Commit: 328bfcd
Notes: clean
