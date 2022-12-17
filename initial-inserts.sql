-- SQLite

-- asset_types table
--INSERT INTO asset_types (id, name)
--VALUES
--  (1, 'Stock'),
--  (2, 'Bond');

-- assets table
--INSERT INTO assets (id, name, type_id)
--VALUES
--  (1, 'Microsoft Corporation', 1),
--  (2, 'Exxon Mobil Corporation', 1),
--  (3, 'Johnson & Johnson', 1);

-- stocks table
--INSERT INTO stocks (asset_id, ticker, exchange, sector, type, industry)
--VALUES
--  (1, 'MSFT', 'NASDAQ', 'Technology', 'Equity', 'Software'),
--  (2, 'XOM', 'NYSE', 'Energy', 'Equity', 'Oil & Gas'),
--  (3, 'JNJ', 'NYSE', 'Healthcare', 'Equity', 'Pharmaceuticals');

-- portfolios table
--INSERT INTO portfolios (id, name, date_created, description)
--VALUES
--  (1, 'Dummy Stock Portfolio', '2018-12-31', 'Equal weight portfolio of stocks');

-- portfolio transactions (initial buy)
-- INSERT INTO portfolio_transactions (id, portfolio_id, asset_id, type, date, quantity, price, description)
-- VALUES
--   (1, 1, 1, 'buy', '2018-12-31', 493, 101.50, 'Microsoft purchase'),
--   (2, 1, 2, 'buy', '2018-12-31', 731, 68.45, 'Exxon purchase'),
--   (3, 1, 3, 'buy', '2018-12-31', 389, 128.50, 'Johnson & Johnson purchase');

-- -- rebalance
-- INSERT INTO portfolio_transactions (id, portfolio_id, asset_id, type, date, quantity, price, description)
-- VALUES
--   (4, 1, 1, 'sell', '2019-01-31', 8, 104.43, 'Microsoft rebalance'),
--   (5, 1, 2, 'buy', '2019-01-31', 18, 73.28, 'Exxon rebalance'),
--   (6, 1, 3, 'sell', '2019-01-31', 4, 133.08, 'Johnson & Johnson rebalance');

-- portfolio_assets (created from portfolio_transactions)
-- INSERT INTO portfolio_assets (portfolio_id, asset_id, last_modified, asset_quantity)
-- SELECT portfolio_id, asset_id, date,
--   (SELECT SUM(CASE WHEN type = 'buy' THEN quantity ELSE -quantity END)
--    FROM portfolio_transactions
--    WHERE asset_id = t.asset_id AND date <= t.date) AS quantity
-- FROM portfolio_transactions t
-- WHERE NOT EXISTS (
--   SELECT 1 FROM portfolio_assets
--   WHERE portfolio_assets.portfolio_id = t.portfolio_id
--     AND portfolio_assets.asset_id = t.asset_id
-- );

