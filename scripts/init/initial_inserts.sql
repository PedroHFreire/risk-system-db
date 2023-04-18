-- SQLite

-- asset_types table
INSERT INTO asset_types (id, name)
VALUES
  (1, 'Cash'),
  (2, 'Stock'),
  (3, 'Bond');

-- assets table
INSERT INTO assets (id, name, type_id)
VALUES
  (1, 'Cash', 1),
  (2, 'Banco do Brasil S.A.', 2),
  (3, 'Petroleo Brasileiro S.A.', 2),
  (4, 'Ambev S.A.', 2);

-- stocks table
INSERT INTO stocks (asset_id, ticker, exchange, sector, type, industry)
VALUES
  (2, 'BBAS3', 'B3', 'Financials', 'Equity', 'Banking'),
  (3, 'PETR4', 'B3', 'Energy', 'Equity', 'Oil & Gas'),
  (4, 'ABEV3', 'B3', 'Consumer Staples', 'Equity', 'Beverages');

-- portfolios table
INSERT INTO portfolios (id, name, date_created, description)
VALUES
  (1, 'Dummy Stock Portfolio', '2018-12-28', 'Equal weight portfolio of stocks');

-- portfolio transactions (initial buy)
 INSERT INTO portfolio_transactions (id, portfolio_id, asset_id, type, date, quantity, price, description)
 VALUES
   (1, 1, 1, 'buy', '2018-12-28', 170000, 1, 'Initial deposit'), 
   (2, 1, 2, 'buy', '2018-12-28', 1440, 34.71, 'Banco do Brasil purchase'),
   (3, 1, 3, 'buy', '2018-12-28', 4806, 10.41, 'Petrobras purchase'),
   (4, 1, 4, 'buy', '2018-12-28', 3670, 13.62, 'Ambev purchase');

-- -- rebalance
 INSERT INTO portfolio_transactions (id, portfolio_id, asset_id, type, date, quantity, price, description)
 VALUES
   (5, 1, 2, 'buy', '2019-12-30', 81, 42.93, 'Banco do Brasil rebalance'),
   (6, 1, 3, 'sell', '2019-12-30', 355, 14.67, 'Petrobras rebalance'),
   (7, 1, 4, 'buy', '2019-12-30', 100, 17.32, 'Ambev rebalance');

-- portfolio_assets (created from portfolio_transactions)
INSERT INTO portfolio_assets (portfolio_id, asset_id, last_modified, asset_quantity)
SELECT portfolio_id, asset_id, date,
   (SELECT SUM(CASE WHEN type = 'buy' THEN quantity ELSE -quantity END)
    FROM portfolio_transactions
    WHERE asset_id = t.asset_id AND date <= t.date) AS quantity
 FROM portfolio_transactions t
 WHERE NOT EXISTS (
   SELECT 1 FROM portfolio_assets
   WHERE portfolio_assets.portfolio_id = t.portfolio_id
     AND portfolio_assets.asset_id = t.asset_id
 );

