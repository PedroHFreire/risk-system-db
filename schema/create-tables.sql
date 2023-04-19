CREATE TABLE portfolios (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  date_created DATE NOT NULL,
  description TEXT
);

CREATE TABLE assets (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  type_id INTEGER NOT NULL,
  FOREIGN KEY (type_id) REFERENCES asset_types(id)
);

CREATE TABLE asset_types (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE portfolio_assets (
  id INTEGER PRIMARY KEY,
  portfolio_id INTEGER NOT NULL,
  asset_id INTEGER NOT NULL,
  asset_quantity INTEGER NOT NULL,
  last_modified DATE NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
  FOREIGN KEY (asset_id) REFERENCES assets(id)
);


CREATE TABLE stocks (
  asset_id INTEGER PRIMARY KEY,
  ticker TEXT UNIQUE NOT NULL,
  exchange TEXT NOT NULL,
  type TEXT,
  sector TEXT NOT NULL,
  subsector TEXT NOT NULL,
  segment TEXT NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE TABLE stock_history (
    asset_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adjusted_close REAL,
    volume INTEGER,
    PRIMARY KEY (asset_id, date),
    FOREIGN KEY (asset_id) REFERENCES assets (id)
);

CREATE TABLE bonds (
  asset_id INTEGER PRIMARY KEY,
  issuer TEXT NOT NULL,
  type TEXT NOT NULL,
  rating TEXT NOT NULL,
  coupon_type TEXT NOT NULL,
  FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE TABLE bond_history (
    asset_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    coupon REAL,
    maturity TEXT,
    yield REAL,
    spread REAL,
    credit_rating TEXT,
    PRIMARY KEY (asset_id, date),
    FOREIGN KEY (asset_id) REFERENCES assets (id)
);

CREATE TABLE portfolio_transactions (
  id INTEGER PRIMARY KEY,
  portfolio_id INTEGER NOT NULL,
  asset_id INTEGER NOT NULL,
  type TEXT NOT NULL,
  date DATE NOT NULL,
  quantity INTEGER NOT NULL,
  price REAL NOT NULL,
  description TEXT,
  FOREIGN KEY (portfolio_id) REFERENCES portfolios(id),
  FOREIGN KEY (asset_id) REFERENCES assets(id)
);

CREATE TABLE portfolio_fees (
  id INTEGER PRIMARY KEY,
  portfolio_id INTEGER NOT NULL,
  fee_type TEXT NOT NULL,
  fee_amount REAL NOT NULL,
  fee_date DATE NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
);

CREATE TABLE portfolio_goals (
  id INTEGER PRIMARY KEY,
  portfolio_id INTEGER NOT NULL,
  goal_type TEXT NOT NULL,
  goal_value REAL NOT NULL,
  goal_description TEXT NOT NULL,
  FOREIGN KEY (portfolio_id) REFERENCES portfolios(id)
);

CREATE TABLE market_indices (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT NOT NULL
);