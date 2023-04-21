import sqlite3
import pandas as pd
import plotly.express as px
import plotly.offline as pyo
from plotly.subplots import make_subplots  # Import the make_subplots function

# Fetch data
## Connect to the database
conn = sqlite3.connect('../risk-system-db/stable.db')

## Fetch the portfolio value over time data
portfolio_value_query = """
WITH asset_prices AS (
    SELECT asset_id, date, close AS price
    FROM stock_history
    WHERE asset_id IN (
        SELECT asset_id
        FROM portfolio_assets
        WHERE portfolio_id = 1
    )
    UNION ALL
    SELECT a.id as asset_id, sh.date, 1 AS price
    FROM assets a
    JOIN stock_history sh ON 1=1
    WHERE a.type_id = (SELECT id FROM asset_types WHERE name = 'Cash')
),
portfolio_value AS (
    SELECT
        ap.date,
        SUM(pa.asset_quantity * ap.price) AS value
    FROM portfolio_assets pa
    JOIN asset_prices ap ON pa.asset_id = ap.asset_id
    WHERE pa.portfolio_id = 1
    GROUP BY ap.date
)
SELECT *
FROM portfolio_value
ORDER BY date;
"""
portfolio_value_df = pd.read_sql_query(portfolio_value_query, conn)

## Fetch the asset allocation data
asset_allocation_query = """
WITH asset_prices AS (
    SELECT sh.asset_id, sh.close AS price
    FROM stock_history sh
    WHERE sh.date = (
        SELECT MAX(date)
        FROM stock_history
        WHERE asset_id = sh.asset_id AND date <= '2022-04-14'
    )
    UNION ALL
    SELECT a.id as asset_id, 1 AS price
    FROM assets a
    WHERE a.type_id = (SELECT id FROM asset_types WHERE name = 'Cash')
)

SELECT at.name as asset_type, SUM(pa.asset_quantity * ap.price) as total_value
FROM portfolio_assets pa
JOIN assets a ON pa.asset_id = a.id
JOIN asset_types at ON a.type_id = at.id
JOIN asset_prices ap ON a.id = ap.asset_id
WHERE pa.portfolio_id = 1
GROUP BY a.type_id, at.name;
"""
asset_allocation_df = pd.read_sql_query(asset_allocation_query, conn)

## Fetch the stock composition data
stock_composition_query = """
WITH asset_prices AS (
    SELECT sh.asset_id, sh.close AS price
    FROM stock_history sh
    WHERE sh.date = (
        SELECT MAX(date)
        FROM stock_history
        WHERE asset_id = sh.asset_id AND date <= '2022-04-14'
    )
)
SELECT
    s.sector,
    s.subsector,
    s.segment,
    a.name as stock,
    SUM(pa.asset_quantity * ap.price) as total_value
FROM portfolio_assets pa
JOIN assets a ON pa.asset_id = a.id
JOIN asset_types at ON a.type_id = at.id
JOIN stocks s ON a.id = s.asset_id
JOIN asset_prices ap ON a.id = ap.asset_id
WHERE pa.portfolio_id = 1 AND at.name = 'Stock'
GROUP BY s.sector, s.subsector, s.segment, a.name;
"""
stock_composition_df = pd.read_sql_query(stock_composition_query, conn)

# Plot charts
## Create plots
portfolio_value_fig = px.line(
    portfolio_value_df,
    x='date',
    y='value',
    title='Portfolio Value Over Time'
)

asset_allocation_fig = px.pie(
    asset_allocation_df,
    values='total_value',
    names='asset_type',
    title='Asset Allocation'
)

stock_composition_fig = px.treemap(
    stock_composition_df,
    path=['sector', 'subsector', 'segment', 'stock'],
    values='total_value',
    title='Stock Composition of the Portfolio',
    width=1000,
    height=600
)

# Create a 2x2 subplot grid with a merged top row
fig = make_subplots(
    rows=2,
    cols=2,
    specs=[
        [{"type": "scatter", "colspan": 2}, None],
        [{"type": "pie"}, {"type": "treemap"}]
    ],
    column_widths=[0.5, 0.5],
    row_heights=[0.5, 0.5],
    subplot_titles=("Portfolio Value Over Time", "Asset Allocation", "Stock Composition")
)

## Add the line chart and pie chart to the subplot grid
fig.add_trace(portfolio_value_fig.data[0], row=1, col=1)
fig.add_trace(asset_allocation_fig.data[0], row=2, col=1)
fig.add_trace(stock_composition_fig.data[0], row=2, col=2)

## Update layout and titles
fig.update_layout(title_text="Portfolio Overview", height=800)

## Render the plot in a browser window
pyo.plot(fig)
