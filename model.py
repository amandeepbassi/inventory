from config import Config
import sqlalchemy as sa

connection = 'postgres://{0}:{1}@{2}/{3}'.format(Config.DATABASE_USER,
                                                 Config.DATABASE_PASSWORD,
                                                 Config.DATABASE_HOST,
                                                 Config.DATBASE_NAME)

milk_produce = sa.Table('tb_raw_milk', sa.MetaData(),
               sa.Column('raw_milk_id', sa.String, primary_key=True),
               sa.Column('raw_milk_timestamp', sa.TIMESTAMP, nullable=False),
               sa.Column('raw_milk_stock', sa.Integer, nullable=False))

p_goods = sa.Table('tb_processed_goods', sa.MetaData(),
               sa.Column('pg_id', sa.String, primary_key=True),
               sa.Column('pg_timestamp', sa.TIMESTAMP, nullable=False),
               sa.Column('pg_product_id', sa.String, nullable=False),
               sa.Column('pg_quantity_produced', sa.Integer, nullable=False),
               sa.Column('pg_quantity_used', sa.Integer, nullable=False))

net_stock = sa.Table('tb_net_stock', sa.MetaData(),
                    sa.Column('net_stock_date', sa.Date, nullable=False),
                    sa.Column('net_stock_value', sa.Integer, nullable=False),
                    sa.Column('net_stock_product_id', sa.String, nullable=False))