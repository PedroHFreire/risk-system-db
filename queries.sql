-- Visualize the portfolio
-- SELECT 
--     portfolios.name AS portfolio_name,
--     assets.name AS asset_name, 
--     stocks.type, 
--     stocks.ticker, 
--     stocks.sector, 
--     stocks.industry
-- FROM portfolio_transactions
-- INNER JOIN assets ON portfolio_transactions.asset_id = assets.id
-- INNER JOIN portfolios ON portfolio_transactions.portfolio_id = portfolios.id
-- INNER JOIN asset_types ON assets.type_id = asset_types.id
-- INNER JOIN stocks ON assets.id = stocks.asset_id
-- WHERE asset_types.name = 'stock';
-- It seems that this script is not working as intended

-- query to get current portfolio
