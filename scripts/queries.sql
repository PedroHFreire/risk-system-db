-- Portfolios history
-- SELECT
--     sh.date,
--     p.name AS portfolio_name, 
--     a.name AS asset_name, 
--     at.name AS type, 
--     sh.adjusted_close AS price, 
--     pa.asset_quantity AS quantity,
--     sh.adjusted_close * pa.asset_quantity AS value
-- FROM portfolio_assets pa
-- JOIN portfolios p ON pa.portfolio_id = p.id
-- JOIN assets a ON pa.asset_id = a.id
-- JOIN asset_types at ON a.type_id = at.id
-- JOIN stock_history sh ON a.id = sh.stock_id
-- JOIN (
--     SELECT portfolio_id, MAX(last_modified) as last_modified
--     FROM portfolio_assets
--     GROUP BY portfolio_id
-- ) t ON pa.portfolio_id = t.portfolio_id AND pa.last_modified = t.last_modified
-- ORDER BY sh.date

-- stock_history adjusted closed prices all assets the portfolio
-- ever had.
SELECT 
    a.name AS asset_name, 
    sh.adjusted_close, 
    sh.date
FROM stock_history sh
JOIN assets a ON sh.stock_id = a.id
JOIN portfolio_assets pa ON pa.asset_id = a.id
WHERE pa.portfolio_id = ?; -- substitute ? by the porfolio you want
