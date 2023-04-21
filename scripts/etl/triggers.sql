-- update portfolio_assets
-- Description: 
-- This trigger will run the UPDATE query whenever
-- a new row is inserted into the portfolio_transactions.
-- This way our current portfolio is always up to date.
CREATE TRIGGER insert_portfolio_assets
AFTER INSERT ON portfolio_transactions
BEGIN
  INSERT INTO portfolio_assets (portfolio_id, asset_id, last_modified, asset_quantity)
  SELECT new.portfolio_id, new.asset_id, new.date,
    (SELECT SUM(CASE WHEN type = 'buy' THEN quantity ELSE -quantity END)
     FROM portfolio_transactions
     WHERE asset_id = new.asset_id AND date <= new.date) AS quantity
  WHERE NOT EXISTS (
    SELECT 1 FROM portfolio_assets
    WHERE portfolio_assets.portfolio_id = new.portfolio_id
      AND portfolio_assets.asset_id = new.asset_id
  );
END;

-- TODO: A trigger that updates the cash balance with each buy or sell