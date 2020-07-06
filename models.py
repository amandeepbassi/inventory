import sqlalchemy as sa

metadata = sa.MetaData()

milk_produced = sa.Table('raw_milk', metadata,
               sa.Column('id', sa.Integer, primary_key=True),
               sa.Column('date', sa.DATE),
               sa.Column('time', sa.TIME),
               sa.Column('raw_milk', sa.Integer),
               sa.Column('stock', sa.Integer)
                         )

p_goods = sa.Table('processed_goods', metadata,
               sa.Column('pg_id', sa.Integer, primary_key=True),
               sa.Column('date', sa.DATE),
               sa.Column('time', sa.TIME),
               sa.Column('product_id', sa.Integer),
               sa.Column('quantity_produced', sa.Integer),
               sa.Column('quantity_used', sa.Integer),
               sa.Column('stock_left', sa.Integer))

