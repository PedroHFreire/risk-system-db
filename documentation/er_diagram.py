from graphviz import Digraph

dot = Digraph('documentation/stabledb_ERD', format='png')
dot.attr(rankdir='LR', size='15')

# Tables
dot.node('A', 'asset_types', shape='rectangle')
dot.node('B', 'assets', shape='rectangle')
dot.node('C', 'portfolios', shape='rectangle')
dot.node('D', 'portfolio_assets', shape='rectangle')
dot.node('E', 'stocks', shape='rectangle')
dot.node('F', 'stock_history', shape='rectangle')
dot.node('G', 'bonds', shape='rectangle')
dot.node('H', 'bond_history', shape='rectangle')
dot.node('I', 'portfolio_transactions', shape='rectangle')
dot.node('J', 'portfolio_fees', shape='rectangle')
dot.node('K', 'portfolio_goals', shape='rectangle')
dot.node('L', 'market_indices', shape='rectangle')

# Relationships
dot.edge('B', 'A', label='type_id')
dot.edge('D', 'C', label='portfolio_id')
dot.edge('D', 'B', label='asset_id')
dot.edge('E', 'B', label='asset_id')
dot.edge('F', 'B', label='asset_id')
dot.edge('G', 'B', label='asset_id')
dot.edge('H', 'B', label='asset_id')
dot.edge('I', 'C', label='portfolio_id')
dot.edge('I', 'B', label='asset_id')
dot.edge('J', 'C', label='portfolio_id')
dot.edge('K', 'C', label='portfolio_id')

# Save and render the output
dot.render('documentation/stabledb_ERD', view=True)
