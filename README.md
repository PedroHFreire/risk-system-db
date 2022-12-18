# Portfolio Management Database

This database is designed for use in an investment software to store and manage portfolio information. It was built using SQLite3 and includes tables for storing information about portfolios, assets, asset types, portfolio assets, stocks, bonds, portfolio transactions, portfolio fees, portfolio goals, and market indices.

The database was built mostly by [Assistant](https://openai.com/blog/openai-assistant/), a large language model trained by OpenAI.

## Directory Structure

- **chats/**: This directory holds chat transcripts with Assistant.
- **schema/**: This directory contains files related to the database schema, including `schema.txt` and `create-tables.sql`.
- **scripts/**: This directory contains SQL and Python scripts for managing the database, including scripts for ETL processes in the `etl/` subdirectory.
- **stable.db**: This is the main database file.

## Tables

- **portfolios**: Stores information about individual portfolios, such as the name and owner of the portfolio.
- **assets**: Stores information about different types of assets, such as stocks and bonds.
- **asset_types**: Stores information about the different asset classes, such as equities and fixed income.
- **portfolio_assets**: Stores information about the assets that are held in each portfolio, including the asset type, quantity, and purchase price. This table is automatically updated whenever there is a portfolio transaction.
- **stocks**: Stores information about individual stocks, such as the ticker symbol and company name.
- **bonds**: Stores information about individual bonds, such as the issuer and coupon rate.
- **stock_history**: Stores historical data for stocks, including the price and volume traded. This table can be updated through a Python script.
- **bond_history**: Stores historical data for bonds, including the price and volume traded.
- **portfolio_transactions**: Stores information about the buy and sell transactions that occur in each portfolio, including the asset type, quantity, and price.
- **portfolio_fees**: Stores information about the fees and expenses associated with each portfolio, such as management fees and trading costs.
- **portfolio_goals**: Stores information about the financial goals and constraints for each portfolio, such as the desired risk level and target return.
- **market_indices**: Stores information about the market indices that you want to use as benchmarks for your portfolio performance, such as the S&P 500 and NASDAQ.

## Features

- Automatically update the `portfolio_assets` table whenever there is a portfolio transaction.
- Update the `stock_history` table through a Python script.

## Usage

This database can be used for storing and managing portfolio information in an investment software, but the same structure could also be used for other purposes.
